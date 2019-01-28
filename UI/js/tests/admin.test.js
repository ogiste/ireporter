import faker from 'faker';
import puppeteer from 'puppeteer';
import testConfig from './testConfig';

const { appUrls, testTimeoutMs } = testConfig;
let browser = ''; let page = '';
jest.setTimeout(testTimeoutMs);
const newIncident = {
  title: `Corruption in ${faker.commerce.department()}`,
  comment: `Corruption in ${faker.commerce.department()} supplier procurement`,
  type: 'red-flag',
  lat: '-1.3534107531208233',
  lng: '36.92142215280501',
};

const admin = {
  username: 'admin',
  password: 'a123456',
};

beforeAll(async () => {
  browser = await puppeteer.launch({
    slowMo: 80,
  });
  page = await browser.newPage();
  page.setDefaultNavigationTimeout(testTimeoutMs)
  await page.goto(appUrls.loginUrl);
  await page.type('input#login_username', admin.username);
  await page.type('input#login_password', admin.password);
  await page.click('button#login_submit');
  await page.waitForNavigation({ timeout: testTimeoutMs, waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#profile');
  await page.$eval('#username', el => el.value);
});

afterAll(() => {
  browser.close();
});

describe('Administrator test set', () => {
  test(' admin can view all created records', async () => {
    await page.goto(appUrls.adminPanelUrl);
    await page.waitForSelector('#incidents_admin_tbody');
    const incidentDetailsContainer = await page.$eval('#incidents_admin_tbody', el => el);
    expect(incidentDetailsContainer).toBeDefined();
  }, testTimeoutMs);

  test(' admin can view all created user details', async () => {
    await page.goto(appUrls.systemUsersUrl);
    await page.waitForSelector('#users_admin_tbody');
    const userDetails = await page.$eval('#users_admin_tbody', el => el);
    expect(userDetails).toBeDefined();
  }, testTimeoutMs);
});
