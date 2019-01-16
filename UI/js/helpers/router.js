import constants from '../constants.js';

const { ireporterSettings } = constants;

function newUrl(urlFilepath = '') {
  const { baseUiUrl } = ireporterSettings;
  console.log('baseUiUrl : ', baseUiUrl);
  location.assign(`${baseUiUrl}/${urlFilepath}`);
}

const router = {
  newUrl,
};

export default router;
