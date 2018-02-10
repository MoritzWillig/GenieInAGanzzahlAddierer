
function UnkownDataType() {

}

UnkownDataType.prototype = Object.create(DataType.prototype);

UnkownDataType.prototype.generateGUIElement = function generateGUIElement(argument) {
    let caption = (argument.caption===undefined)?"Unkown":argument.caption;
    let defaultValue = (argument.defaultValue===undefined)?"":argument.defaultValue;

    var container = document.createElement("div");
    container.innerHTML=caption+": <input>"+defaultValue+"</input>";
    return container;
};