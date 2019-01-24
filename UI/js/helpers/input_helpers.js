// document.querySelector('#searchTxt').value;

function getElById(element_id = '') {
  // Function that takes the element id value and returns its value
  return document.getElementById(element_id);
}

function setElTextById(element_id = '', elementText = '') {
  getElById(element_id).innerHTML = elementText;
}

const inputHelpers = {
  getElById,
  setElTextById,
};

export default inputHelpers;
