import authHelpers from './helpers/auth_helpers.js';
import router from './helpers/router.js';
import domHelpers from './helpers/dom_helpers.js';
import alerts from './components/alerts.js';
import constants from './constants.js';

const { alertIds } = constants;
const { isAuth, getAuthProfile } = authHelpers;
const { setElTextById } = domHelpers;
const { newUrl, uiUrlFilepaths } = router;
const { createAlert } = alerts;

function loadProfilePage(userProfile) {
  // Function to load profile page with user profile data for current userData
  if (userProfile) {
    setElTextById('username', userProfile.username);
    setElTextById('user_fname', userProfile.fname);
    setElTextById('user_lname', userProfile.lname);
    setElTextById('user_othername', userProfile.othername);
    setElTextById('user_email', userProfile.email);
    setElTextById('user_phone', userProfile.phone);
  }
}

function getUserProfile() {
  // Function that loads user profile data to page
  createAlert('loading...', alertIds.loading);
  if (isAuth()) {
    createAlert('Profile loaded', alertIds.success);
    const userProfile = getAuthProfile();
    loadProfilePage(userProfile);
    return;
  }
  createAlert('You are not signed in', alertIds.error);
  newUrl(uiUrlFilepaths.LOGIN);
}

getUserProfile();
