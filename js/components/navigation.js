import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import domHelpers from '../helpers/dom_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import constants from '../constants.js';
import mapsApi from '../maps.js';

const { geocodeLatLng, geocoder, infowindow, initMap } = mapsApi;
const { uiUrlFilepaths, isCurrentRoute } = router;
const {
  getElTextValue,
  getElById,
  setElTextById,
  getSelectedInputOption,
  createDomElement
} = domHelpers;
const { isAuth, isAdmin } = authHelpers;

function displayAdminNavItems() {
  // Function used to display Navigation items for admin users
  const navList = getElById('main_nav_ul');
  if (isAuth() && isAdmin() && !isCurrentRoute(uiUrlFilepaths.REGISTER)
  && !isCurrentRoute(uiUrlFilepaths.LOGIN)
  && !isCurrentRoute(uiUrlFilepaths.ADMIN)) {
    console.log('displayAdminNavItems :true');
    console.log('pathname: ', window.location.pathname);
    const adminPageListItem = createDomElement('li');
    const adminPageLink = createDomElement('a', 'Administrator Panel');
    adminPageLink.href = `${uiUrlFilepaths.ADMIN}`;
    adminPageListItem.appendChild(adminPageLink);
    navList.appendChild(adminPageListItem);
  }
}

function displayHomeNavItems() {
  // Function used to display Navigation items for admin users
  const navList = getElById('main_nav_ul');
  if (isAuth() && isCurrentRoute(uiUrlFilepaths.HOME)) {
    navList.innerHTML = '';
    const profilePageListItem = createDomElement('li');
    const profilePageLink = createDomElement('a', 'My Profile');
    profilePageLink.href = `${uiUrlFilepaths.PROFILE}`;
    profilePageListItem.appendChild(profilePageLink);
    navList.appendChild(profilePageListItem);
    const logoutListItem = createDomElement('li');
    logoutListItem.className += ' li-right';
    const logoutLink = createDomElement('a', 'Logout', '', 'logout_link');
    logoutListItem.appendChild(logoutLink);
    navList.appendChild(logoutListItem);
    console.log('navList: ', navList);
  }
}

const navigationComponents = {
  displayAdminNavItems,
  displayHomeNavItems,
};

export default navigationComponents;
