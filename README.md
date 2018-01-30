# GenieInAGanzzahlAddierer

![Genie Eye Logo](./static/media/images/eye.png "Genie Eye Logo")

This software project helps to provide basic user interfaces for console applications.


## Quick start
This projects provides a CommandLineGenie class, which is capable of calling arbitrary commandline scripts. It should provide enough functionality to run most command-line binaries. For more complex tasks, writing a customized Genie is the other, more advanced, option. Writing your own genie gives you full control of the assembly and execution of the final commandline. A detailed description can be found under {Software overview / Genies}. To create an UI for simple command-line tools follow the steps below.

## 0. install dependencies
```
pip install flask
```
``numpy Pillow`` are required for the demo script under `demo/`
 
## 1. create a new genie

Create a new `my_genie_name.json` file under `configurations/` (or copy the already existing `format.json`). Edit the `info`-attribute to describe your genie in short. The commandline that will be called by the genie will for each request is assembled from the `arguments`-attribute. To adjust the `arguments`-attribute to match your commandline tool, see the {Software overview / Data Types} section. The system will automatically manage in- and output files and/or folders.

Each block has to contain a `type` attribute and type specific attributes. Most commandlines should start with a `plain` block, which defines the binary to be executed: 
```
{
  "type": "plain",
  "text": "python ./demo/image_color.py"
}
```

A list of input and output arguments typically follows:
```
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
Input or output arguments a characterized by adding an `semantic`-attribute set to `in` or `out`. For each of these, a unique `id` has to be set. These ids are used by the API when sending input values or files, or when serving output files. The `creation` attribute is specific to the image type (see {Software overview / Data Types / Image}). Most common types, like `boolean`, `int`, `file_folder` are already implemented. Look into the code and/or documentation to see the type specific attributes that can be added, to e.g. perform input checks (for example allow only `min: 1` and `max: 10`).

### 1.2 Filters

If os specific parts are required for the commandline, a `filter`-attribute can be added: 
```
{
  "type": "plain",
  "text": "-argument_for_windows",
  "filter": {
    "os": "windows"
  }
}
```
The strings will be matches against `platform.system()`. Allowed values are e.g. `windows`, `linux`, `java`.

## 2. register genie

Add a new entry to `arguments` in the `config.json`. 
```
{
  "name": "my_genie_name",
  "genie": "abstract.commandLine",
  "configuration": "configurations/my_genie_name.json"
}
```
* `name` is the name under which the genie will be exposed through the API.
* `genie` is the genie to load. The genies will be loaded from `src\genies` (See {Software overview / Genies} for a detailed description). Use `abstract.commandLine` for the generic commandline genie or any of your custom genies.
* `configuration` - a custom configuration file to pass to the genie.

## API
The software provides an json - API interface for session management and executing genie actions. Each genie action requested operates inside a session folder, managed by the software. Upon requesting a genie action for a session, using `/genie/<genie_name>/request/<session_name>`, a check for the presense of all required arguments is performed. The required arguments for each genie can be requested via `/genie/<genie_name>/interface`. The result of the request contains a status code and additional information dependent on the specific genie (e.g. available output files). Output files can then be requested via `/session/<session_name>/serve/<data_id>`.

### user interface
* **static files**  
  URL: `/`  
  
  Serves the contents of the `static` folder as a website.

### Sessions
* **create a new session**  
  URL: `/session/create`  
  
  Create a new session to upload files and perform genie actions  
  result upon success:
```
{
  "session": "<session_name>",
  "success": true
}
```

* **upload an input file**  
  URL: `/session/<session_name>/upload/<input_id>`  
  
  Upload a file into a session. The file is stored to the session folder and will be automatically included when requesting a genie action for this session.  
  result upon success:
```
{
  "message": "ok",
  "success": true
} 
```
  
* **request an output file / parameter**  
  URL: `/session/<session_name>/serve/<data_id>`  
  
  This API call parses and directly passes the argument to the genie by value. For passing files, use `/session/<session_name>/upload/<input_id>`!

```
{ "response": { "error": 0, "request": "user_static", "results": { "results": { "data": [ "user_static/000.png", "user_static/001.png", "user_static/002.png", "user_static/003.png" ], "type": "image_folder" } } }, "success": true } 
```

### Genies
* **interface**  
  URL: `/genie/<genie_name>/interface`  
  
  Provides the input and output parameter ids and data types for a genie.   
  result upon success:  
```
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
  
  Performs a genie action on the session. Notice that, unlike all other API-requests, the result is not in JSON format. Resulting output files, like images, can be directly served this way.

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

