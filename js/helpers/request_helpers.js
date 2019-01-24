

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
    for (const propKey in Object.keys(resData)) {
      if ( typeof resData[propKey] === 'object' && propKey ==="message" &&
      resData[propKey] !== null ) {
        console.log('propKey: ',propKey);
        console.log('resData[propKey]: ',resData[propKey]);
        errorMessages.push(getValidationErrorMessage(resData[propKey]));
      }
      if ( typeof resData[propKey] === 'string' &&
      resData[propKey] !== '') {
        return resData[propKey];
      }
    }
  }
  const allValidationErrors = errorMessages;
  const validationErrorMessage = getErrorString(allValidationErrors);
  errorMessages = [];
  return validationErrorMessage;
}
// function postData(url = '', data = {}, reqHeaders = {}) {
//   // Function used to post data using the fetch API
//   console.log('postData url: ', url);
//   console.log('postData data: ', data);
//   console.log('postData reqHeaders: ', reqHeaders);
//   return fetch(url, {
//     method: 'POST',
//     mode: 'cors',
//     headers: reqHeaders,
//     body: JSON.stringify(data),
//   }).then(((response) => {
//     console.log('postData: ', response.json());
//     // const res = response.json();
//     // if (!Object.prototype.hasOwnProperty.call(res, 'status_code')) {
//     //   res.status_code = response.status;
//     // }
//     return response.json();
//   }));
// }
function postData(url = '', data = {}, reqHeaders = {}) {
  // Function used to post data using the fetch API
  console.log(JSON.stringify(data));
  return fetch(url, {
    method: 'POST',
    headers: reqHeaders,
    body: JSON.stringify(data),
  }).then(response => response.json());
}

function getData(url = '', reqHeaders = {}) {
  // Function used to post data using the fetch API
  return fetch(url, {
    method: 'GET',
    mode: 'cors',
    headers: reqHeaders,
  }).then(response => response.json());
}

const reqHelpers = {
  postData,
  getData,
  getValidationErrorMessage,
};

export default reqHelpers;
