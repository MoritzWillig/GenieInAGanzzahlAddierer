
function IntDataType() {

}

IntDataType.prototype = Object.create(DataType);

IntDataType.prototype.generateGUIElement = function generateGUIElement(argument) {
    let caption = (argument.caption===undefined)?"Integer":argument.caption;
    let defaultValue = (argument.defaultValue===undefined)?"":argument.defaultValue;

    var container = document.createElement("div");
    container.innerHTML=caption+": <input>"+defaultValue+"</input>";
    return container;
};