// document.querySelector('#searchTxt').value;

function getElById(element_id = '') {
  // Function that takes the element id value and returns its value
  return document.getElementById(element_id).value;
}

const userInputHelpers = {
  getElById,
};

export default userInputHelpers;
