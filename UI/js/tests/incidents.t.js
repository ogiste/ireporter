const faker = require("faker");
const puppeteer = require("puppeteer");
var browser, page;

const state = {
  title: "Jest Testing",
  record_type: "intervention",
  location: faker.address.state(),
  comment: faker.lorem.paragraphs(),
  status: "draft"
};

beforeEach(async () => {
  browser = await puppeteer.launch();
  page = await browser.newPage();
  console.log('loaded setup');
});

describe('iReporter New Incident', () => {
  describe('Page on form submit ', () => {
    beforeEach(async () => {
      await page.goto(
        "https://bl4ck4ndbr0wn.github.io/iReporter/UI/create-incident.html"
      );
    }, 10000);
    it("User should be able to login with correct credentials", async () => {
      await page.click("input#auth_username");
      await page.type("input#auth_username", "alpha");

      await page.click("input#auth_password");
      await page.type("input#auth_password", "Ak3Swal(");

      await page.click("input#login_submit");

      await page.waitForSelector("#popuptextmsg");
      const message = await page.$eval(
        "#popuptextmsg",
        response => response.innerText
      );
      expect(message).toMatch("You were successfully logged in alpha");
    }, 100000);

    // it("User should be able to create a new incident record", async () => {
    //   await page.click("input#title");
    //   await page.type("input#title", state.title);

    //   await page.click("input#record_type");
    //   await page.type("input#record_type", state.record_type);

    //   await page.click("input#comment");
    //   await page.type("input#comment", state.comment);

    //   await page.click("input#location");
    //   await page.type("input#location", state.location);

    //   await page.click("input#incident_submit");

    //   await page.waitForSelector("#popuptextmsg");
    //   const message = await page.$eval(
    //     "#popuptextmsg",
    //     response => response.innerText
    //   );
    //   expect(message).toMatch("Incident created Successfully.");
    // }, 10000);
  }, 10000);
}, 10000);

afterEach(async () => {
  await browser.close();
});
