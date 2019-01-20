
// import * as reqHelpers from './helpers/request_helpers';
import inputHelpers from './helpers/input_helpers.js';
import userServices from './services/user_services.js';

const { login, logout, register } = userServices;
const { getElById } = inputHelpers;
if (getElById('register_submit')) getElById('register_submit').addEventListener('click', register);
if (getElById('login_submit')) getElById('login_submit').addEventListener('click', login);
if (getElById('logout_link')) getElById('logout_link').addEventListener('click', logout);
