

function postData(url = '', data = {}, reqHeaders = {}) {
  // Function used to post data using the fetch API
  console.log(data);
  return fetch(url, {
    method: 'POST',
    mode: 'cors',
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
};

export default reqHelpers;
