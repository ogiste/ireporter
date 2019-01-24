// document.querySelector('#searchTxt').value;

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

const inputHelpers = {
  getElById,
  setElTextById,
  getElTextValue,
  getSelectedInputOption,
};

export default inputHelpers;
