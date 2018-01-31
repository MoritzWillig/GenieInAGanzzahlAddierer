# GenieInAGanzzahlAddierer

![Genie Eye Logo](https://github.com/MoritzWillig/GenieInAGanzzahlAddierer/raw/master/static/media/images/eye.png "Genie Eye Logo")

This software project helps to provide basic user interfaces for image processing console applications.


## Quick start
This projects provides a `CommandLineGenie` class, which is capable of calling arbitrary command line scripts. It should provide enough functionality to handle most command-line binaries. For more complex tasks, writing a customized Genie is the other, more advanced, option. Writing your own genie gives you full control of the assembly and execution of the final command line. A detailed description can be found under {Software overview / Genies}. Follow the steps below, to quickly setup the project and create a first UI for simple command-line tools.

## 0. Install dependencies and setup the configuration
```
pip install flask
```
``numpy Pillow`` are required to run example code requiring the demo script under `demo/`.

### Configuration
The configuration file `config.json` has to be located in the root project folder. An already existing example configuration file `config.sample.json` can be copied and/or renamed. By default most settings should be left unchanged. Custom genies can be added with a new entry to the `genies`-attribute. This step is shown in {2. register the genie}. Definitions of unused genies can be removed from the list or disabled by adding `"ignore": true` to the corresponding configuration entry.

For development and debugging the following lines can be added to get more verbose logging information:
```json
"dev": {
  "enable": true
}
```

## 1. Create a new genie
Create a new `my_genie_name.json` file under `configurations/` (or copy the already existing `format.json`). Edit the `info`-attribute to describe your genie in short. The shell command, that will be called for each request by the genie, is assembled from the `arguments`-list. To adjust the `arguments`-attribute to match your command line tool, see the {Software overview / Data Types} section. Each block in the list is preprocessed by the genie and then appended to the command line string. The system will automatically manage the creation of in- and output files and folders for you.
* **Warning**: Currently there is no authentification required and no limitation is made in terms of the number of existing sessions. We therefore strongly advice you to add a custom authentification method or othwise **do not open the server to public networks**.
* **Warning**: By default, the web server only listens to the link local interface (`localhost`/`127.0.0.1`). If you, for any reason, decide to open the server for public access, make sure that all active genies only **work with binaries, without any known vulnerabilities**.
* **Warning**: Some user inputs, like e.g. file names, are automatically sanitized by the software. There is however no way to automatically perform a semantic check of the input values. If you have an input parameter, that, for example, determines the number of resulting pictures, you should define an upper limit, by adding a `max`-attribute to your parameter definition. All data types support those **filters and bounds checks to sanitize the user input** and keep your system safe and secure.

Each block must contain a `type` attribute followed by type specific attributes. Most shell commands should start with a `plain` block, which defines the binary to be executed:
```json
{
  "type": "plain",
  "text": "python ./demo/image_color.py"
}
```

Typically, a list of input and output arguments follows:
```json
{
  "type": "plain",
  "text": " -in="
},
{
  "id": "source",
  "type": "image",
  "semantic": "in",
  "creation": "existing"
}
```

Input or output arguments are characterized by adding a `semantic`-attribute set to `in` or `out`. For each of these, a unique `id` has to be set. These ids are used by the API when sending input values or files, or when serving output files. The `creation` attribute is specific to the image type (see {Software overview / Data Types / Image}) and states, that the file is expected to be provided by the user (-> no automatic creation by the system). Most common types, like `boolean`, `int`, `file_folder` are already implemented. Look into the code and/or documentation to see the type specific attributes that can be added, to e.g. perform input checks (for example allow only `min: 1` and `max: 10` for integers).

### 1.2 System specific command lines
If OS specific parts are required, a `filter`-attribute can be added to include certain blocks for some platforms only:
```json
{
  "type": "plain",
  "text": "-special_windows_specific_flag",
  "filter": {
    "os": "windows"
  }
}
```
The `os`-string will be matched against `platform.system()`. Therefore, allowed values are `windows`, `linux`, `java`.

## 2. Register the genie
Add a new entry to the `genies`-list in the `config.json`.
```json
{
  "name": "my_genie_name",
  "genie": "abstract.commandLine",
  "configuration": "configurations/my_genie_name.json"
}
```
* `name` is the name under which the genie will be exposed by the API.
* `genie` is the genie name to load. The genies will be loaded from `src/genies` (See {Software overview / Genies} for a detailed description). Use `abstract.commandLine` for the generic commandline genie, or the name of any of your custom genies.
* `configuration` - the custom configuration file created in step {1. create a new genie} to setup the genie.

## API
The software provides an json-API interface for session management and executing genie actions. Each requested genie action operates inside a session folder which is managed by the software. Upon requesting a genie action for a session, using `/genie/<genie_name>/request/<session_name>`, a presence check for all required arguments is performed. The required arguments for each genie can be requested via `/genie/<genie_name>/interface`. The result of the request contains a status code and additional information dependent on the specific genie (e.g. available output files). Output files can then be requested via `/session/<session_name>/serve/<data_id>`.

### User interface
* **static files**  
  URL: `/`  

  Serves the contents of the `static` folder as a website.

### Sessions
* **create a new session**  
  URL: `/session/create`  

  Create a new session to upload files and perform genie actions.  
  result upon success:
  ```json
  {
    "session": "<session_name>",
    "success": true
  }
  ```

* **upload an input file**  
  URL: `/session/<session_name>/upload/<input_id>`  

  Upload a file into a session. The file is stored to the session folder and will be automatically included when requesting a genie action for this session.  
  result upon success:
  ```json
  {
    "message": "ok",
    "success": true
  }
  ```

* **request an output file / parameter**  
  URL: `/session/<session_name>/serve/<data_id>`  

  Serves the output files or values of an genie action.  
  **Notice** that, unlike all other API-requests, this API-call serves raw data, and therefore is not in JSON format. Resulting output files, like images, can be directly included into websites this way.


### Genies
* **interface**  
  URL: `/genie/<genie_name>/interface`  

  Provides the input and output parameter ids and data types for a genie.  
  result upon success:  
  ```json
  {
    "inputs": {
      "num_images": "int",
      "source": "image"
    },
    "outputs:": {
      "results": "image_folder"
    }
  }
  ```

* **request a genie action**  
  URL: `/genie/<genie_name>/request/<session_name>`  
  Parameters: GET/POST: input parameters for the genie  

  This API call parses and directly passes the argument to the genie by value. For passing files, use `/session/<session_name>/upload/<input_id>`!  
  result upon success:  
  ```json
  {
    "response": {
      "error": 0,
      "request": "<session_name>",
      "results": {
        "results": {
          "type": "image_folder",
          "data": [ "user_static/000.png", "user_static/001.png"]
        }
      }
    },
    "success": true
  }
  ```


## Software overview

TODO

### Folder structure
Folder structure and important files
```
├ .temp                        - session storage
├ configurations               - genie configuration files
├ demo                         - demo script
├ external                     - folder for external script (e.g. projects / scripts run by genies)
├ src                          - source code
  ├ datatypes                    - input / output argument processing
  ├ fileManager                  - session and file managment
  ├ genies                       - genie implementations
  ├ helpers                      - helper files
  | GenieInterface.py            - interface for all Genies
  └ main.py                      - web server
├ static                       - files served to client-side
| config.json                  - active config (see quick start)
| config.sample.json           - sample config
| genieIAGA.py                 - startup script
└ README.md                    - readme
```

### Genies

#### CommandlineGenie

asdf

### Data Types

### Sessions

### Configuration
