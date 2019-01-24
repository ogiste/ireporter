import constants from '../constants.js';

const { ireporterSettings } = constants;

function newUrl(urlFilepath = '') {
  // Function to change the browser location to a new url by taking in
  // urlFilepath string and appending it to current bas UI url.
  const { baseUiUrl } = ireporterSettings;
  console.log('baseUiUrl : ', baseUiUrl);
  location.assign(`${baseUiUrl}/${urlFilepath}`);
}

function isCurrentRoute(candidateUiUrlFilePath) {
  // Function that returns a bool value based on if the current page
  // is the page for a particular route
  if (window.location.pathname === `/ireporter/UI/${candidateUiUrlFilePath}`) {
    return true;
  }
  return false;
}

const uiUrlFilepaths = {
  HOME: 'index.html',
  LOGIN: 'login.html',
  REGISTER: 'sign_up.html',
  PROFILE: 'profile.html',
  NEW_INCIDENT: 'create_quest.html',
  EDIT_INCIDENT: 'edit_quest.html',
  ADMIN: 'admin.html',
  USERS: 'users.html',
  VIEW_ALL_INCIDENTS: 'view_my_quests.html',
  VIEW_INCIDENT: 'view_quest.html',
};

const router = {
  newUrl,
  uiUrlFilepaths,
  isCurrentRoute,
};

export default router;
