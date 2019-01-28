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

const user = {
  username: 'notadmin',
  password: 'a123456',
};

beforeAll(async () => {
  browser = await puppeteer.launch({
    slowMo: 80,
  });
  page = await browser.newPage();
  page.setDefaultNavigationTimeout(testTimeoutMs)
  await page.goto(appUrls.loginUrl);
  await page.type('input#login_username', user.username);
  await page.type('input#login_password', user.password);
  await page.click('button#login_submit');
  await page.waitForNavigation({ timeout: testTimeoutMs, waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#profile');
  await page.$eval('#username', el => el.value);
});

afterAll(() => {
  browser.close();
});

describe('Incident Test Set - Incident Creation and View', () => {
  test(' User can create an incident', async () => {
    await page.goto(appUrls.createIncidentUrl);
    await page.waitForSelector('#quest_create');
    await page.type('input#new_incident_title', newIncident.title);
    await page.type('textarea#new_incident_comment', newIncident.comment);
    await page.select('select#new_incident_type', newIncident.type);
    await page.type('input#incident_lat', newIncident.lat);
    await page.type('input#incident_lng', newIncident.lng);
    await page.click('button#new_incident_submit');
    await page.waitForNavigation({ timeout: testTimeoutMs, waitUntil: 'domcontentloaded' });
    const incidentDetailsContainer = await page.$eval('#incident_container', el => el);
    expect(incidentDetailsContainer).toBeDefined();
  }, testTimeoutMs);

  test(' User can view created incident details', async () => {
    await page.waitForSelector('#incident_container');
    const incidentTitle = await page.$eval('#incident_title', el => el.value);
    expect(incidentTitle).toBe(newIncident.title);
  }, testTimeoutMs);
});
