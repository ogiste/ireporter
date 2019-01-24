
let resStatus = '';
let errorMessages = [];
function getErrorString(allValidationErrors) {
  // Function to return a generated error string message from the array of
  // validation error messages
  let errorString = '';
  if (allValidationErrors.length > 1) {
    for (let i = 0; i < allValidationErrors.length; i++) {
      if (i === allValidationErrors.length - 1) {
        errorString += ` ${allValidationErrors[i]} `;
      }
      errorString += ` ${allValidationErrors[i]}, `;
    }
    return errorString;
  }
  if (allValidationErrors.length === 1) {
    errorString += ` ${allValidationErrors[0]}. `;
    return errorString;
  }
  return errorString;
}

function getValidationErrorMessage(resData) {
  // recursive function that returns the message string from a response with
  // a different error message format
  if (typeof resData === 'object' && resData !== null) {
    const propKeys = Object.keys(resData);
    let propName = '';
    for (let propKey = 0; propKey < propKeys.length; propKey++) {
      propName = propKeys[propKey];
      if (typeof resData[propName] === 'object' && propName === 'message'
      && resData[propName] !== null) {
        errorMessages.push(getValidationErrorMessage(resData[propName]));
      }
      if (typeof resData[propName] === 'string'
      && resData[propName] !== '') {
        return resData[propName];
      }
    }
  }
  const allValidationErrors = errorMessages;
  const validationErrorMessage = getErrorString(allValidationErrors);
  errorMessages = [];
  return validationErrorMessage;
}

function postData(url = '', data = {}, reqHeaders = {}) {
  // Function used to post data using the fetch API
  return fetch(url, {
    method: 'POST',
    mode: 'cors',
    headers: reqHeaders,
    body: JSON.stringify(data),
  }).then((res) => {
    resStatus = res.status;
    return res.clone().json();
  }).then(((response) => {
    console.log('postData: ', response);
    let res = response;
    if (!Object.prototype.hasOwnProperty.call(res, 'status_code')) {
      res['status_code'] = resStatus;
    }
    return res;
  }));
}

function patchData(url = '', data = {}, reqHeaders = {}) {
  // Function used to post data using the fetch API
  return fetch(url, {
    method: 'PATCH',
    mode: 'cors',
    headers: reqHeaders,
    body: JSON.stringify(data),
  }).then((res) => {
    resStatus = res.status;
    return res.clone().json();
  }).then(((response) => {
    console.log('patchData: ', response);
    let res = response;
    if (!Object.prototype.hasOwnProperty.call(res, 'status_code')) {
      res['status_code'] = resStatus;
    }
    return res;
  }));
}


function getData(url = '', reqHeaders = {}) {
  // Function used to post data using the fetch API
  return fetch(url, {
    method: 'GET',
    headers: reqHeaders,
  }).then((res) => {
    resStatus = res.status;
    return res.clone().json();
  }).then(((response) => {
    console.log('getData: ', response);
    let res = response;
    if (!Object.prototype.hasOwnProperty.call(res, 'status_code')) {
      res['status_code'] = resStatus;
    }
    return res;
  }));
}

function deleteData(url = '', reqHeaders = {}) {
  // Function used to post data using the fetch API
  return fetch(url, {
    method: 'DELETE',
    headers: reqHeaders,
  }).then((res) => {
    resStatus = res.status;
    return res.clone().json();
  }).then(((response) => {
    console.log('deleteData: ', response);
    let res = response;
    if (!Object.prototype.hasOwnProperty.call(res, 'status_code')) {
      res['status_code'] = resStatus;
    }
    return res;
  }));
}

const reqHelpers = {
  postData,
  patchData,
  getData,
  deleteData,
  getValidationErrorMessage,
};

export default reqHelpers;
