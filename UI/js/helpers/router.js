import constants from '../constants.js';

const { ireporterSettings } = constants;

function newUrl(urlFilepath = '') {
  // Function to change the browser location to a new url by taking in
  // urlFilepath string and appending it to current bas UI url.
  const { baseUiUrl } = ireporterSettings;
  console.log('baseUiUrl : ', baseUiUrl);
  location.assign(`${baseUiUrl}/${urlFilepath}`);
}

const uiUrlFilepaths = {
  HOME: 'index.html',
  LOGIN: 'login.html',
  REGISTER: 'sign_up.html',
  PROFILE: 'profile.html',
  NEW_INCIDENT: 'create_quest.html',
  EDIT_INCIDENT: 'edit_quest.html',
  ADMIN: 'admin.html',
  VIEW_ALL_INCIDENTS: 'view_my_quests.html',
  VIEW_INCIDENT: 'view_quest.html',
};

const router = {
  newUrl,
  uiUrlFilepaths,
};

export default router;
