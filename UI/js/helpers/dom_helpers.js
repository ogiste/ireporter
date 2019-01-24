// document.querySelector('#searchTxt').value;
function createDomElement(elementTag = 'div', elementText = '', elementClass = '',
  elementId = '') {
  // Function to create a new DOM element and return the created element
  const newElement = document.createElement(elementTag);
  // newElement.classList.add(`${elementClass}`);
  newElement.className += ` ${elementClass}`;
  newElement.id = elementId;
  const elementTextNode = document.createTextNode(elementText);
  newElement.appendChild(elementTextNode);
  return newElement;
}

function getElById(element_id = '') {
  // Function that takes the element id value and returns its value
  return document.getElementById(element_id);
}

function setElTextById(element_id = '', elementText = '') {
  if (getElById(element_id)) {
    if (getElById(element_id) instanceof HTMLInputElement
     && (getElById(element_id).type === 'text'
     || getElById(element_id).type === 'textbox')) {
      getElById(element_id).value = elementText;
      return;
    }
    getElById(element_id).innerHTML = elementText;
  }
}

function getElTextValue(element_id = '') {
  // Function to return the text value of a HTML element
  if (getElById(element_id)) {
    if (getElById(element_id).type === 'text'
     || getElById(element_id).type === 'textarea'
     || getElById(element_id).type === 'password') {
      return getElById(element_id).value;
    }
    return getElById(element_id).innerHTML;
  }
  return '';
}

function getSelectedInputOption(element_id = '') {
  // Function to return the selected option's text value
  if (getElById(element_id)) {
    const inputSelectElement = getElById(element_id);
    const selectedOption = inputSelectElement
      .options[inputSelectElement.selectedIndex].value;
    return selectedOption;
  }
  return '';
}

function getElementByAttribute(attributeName = '', attributeValue = '') {
  // Function used to return the first element matching an attribute based query
  // using the attibute name and attribute value as search parameters
  return document.querySelector(`[${attributeName}="${attributeValue}"]`);
}

function addElementClassEventListener(eventCallback, elementClass = '') {
  // Function used to add event listeners to all delete buttons
  const elementLinks = document.getElementsByClassName(elementClass);
  const elementsArray = Array.from(elementLinks);
  elementsArray.forEach((element) => {
    element.addEventListener('click', eventCallback);
  });
}


const domHelpers = {
  getElById,
  setElTextById,
  getElTextValue,
  getSelectedInputOption,
  getElementByAttribute,
  createDomElement,
  addElementClassEventListener,
};

export default domHelpers;