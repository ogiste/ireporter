import faker from 'faker';
import puppeteer from 'puppeteer';
import testConfig from './testConfig';

const { appUrls, testTimeoutMs } = testConfig;
let browser = ''; let page = 'pagestring';
const width = 1366;
const height = 768;

jest.setTimeout(testTimeoutMs);

function generateRandomPhone() {
  // Function to generate a random user phone number
  const set1 = Math.floor(Math.random() * 11) + 10;
  const set2 = Math.floor(Math.random() * 101) + 100;
  const set3 = Math.floor(Math.random() * 101) + 200;
  return `+2547${set1}${set2}${set3}`;
}

const newUser = {
  username: faker.fake('{{name.firstName}}{{random.number}}'),
  fname: faker.name.firstName(),
  lname: faker.name.lastName(),
  othername: faker.name.firstName(),
  email: faker.internet.email(),
  phone: generateRandomPhone(),
  password: 'a123456',
};

beforeAll(async () => {
  browser = await puppeteer.launch({
    slowMo: 80,
  });
  page = await browser.newPage();
  page.setDefaultNavigationTimeout(testTimeoutMs)
  await page.goto(appUrls.homeUrl);
});

afterAll(() => {
  browser.close();
});

describe('First User Test Set - User Registration and Login', () => {
  test(' User can create an account', async () => {
    await page.goto(appUrls.registerUrl);
    await page.waitForSelector('.sign_up_form');
    await page.type('input#sign_up_username', newUser.username);
    await page.type('input#sign_up_fname', newUser.fname);
    await page.type('input#sign_up_lname', newUser.lname);
    await page.type('input#sign_up_othername', newUser.othername);
    await page.type('input#sign_up_email', newUser.email);
    await page.type('input#sign_up_phone', newUser.phone);
    await page.type('input#sign_up_password', newUser.password);
    await page.click('button#register_submit');
    await page.waitForNavigation({ timeout: testTimeoutMs, waitUntil: 'domcontentloaded' });
    const loginPageElement = await page.$eval('#login_username', el => el);
    expect(loginPageElement).toBeDefined();
  }, testTimeoutMs);

  test(' User can login using their account details', async () => {
    await page.type('input#login_username', newUser.username);
    await page.type('input#login_password', newUser.password);
    await page.click('button#login_submit');
    await page.waitForNavigation({ timeout: testTimeoutMs, waitUntil: 'domcontentloaded' });
    await page.waitForSelector('#profile');
    const profileUsername = await page.$eval('#username', el => el.value);
    expect(profileUsername).toBe(newUser.username);
  }, testTimeoutMs);
});
