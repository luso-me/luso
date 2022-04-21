import "cypress-localstorage-commands";

const userId = Cypress.env("userId");
const prefix = "plan-create-";

describe("Plan Create Page", () => {

  beforeEach(() => {
    cy.restoreLocalStorage();
  });



  it("should handle save skill resource dialog - new", () => {
    cy.visit(`/plans/${userId}/create`);

    selectSkill("Apache Airflow");
    selectTimeHorizon("1 week - 3 months");

    cy.getBySel(prefix + "select-skill-resource-dialog")
    .contains('Learn Amazing Airflow Now').click();

    // select 2nd row
    selectResourceDialogRow(1);

    saveResourceDialogAndAssert(0,
        "Learn Amazing Airflow Now", "Chapter 2: Hello World");

    // start mission
    cy.getBySel(prefix + "start-mission").should('be.enabled');
    cy.getBySel(prefix + "form").submit();
  });


  it("should handle save skill resource dialog - delete, add", () => {
    cy.visit(`/plans/${userId}/create`);

    selectSkill("Apache Airflow");
    selectTimeHorizon("3 - 6 months");

    cy.getBySel(prefix + "select-skill-resource-dialog")
    .contains('Learn Amazing Airflow Now').click();

    // select 2nd row
    selectResourceDialogRow(1);

    saveResourceDialogAndAssert(0,
        "Learn Amazing Airflow Now", "Chapter 2: Hello World");

    // show dialog again
    cy.getBySel(prefix + "select-skill-resource-dialog")
    .contains('Learn Amazing Airflow Now').click();

    selectResourceDialogRow(0);
    selectResourceDialogRow(1);

    saveResourceDialogAndAssert(0,
        "Learn Amazing Airflow Now", "Chapter 1: Introduction to Airflow");
  });

  function selectSkill(name: string) {
    cy.getBySel(prefix + "select-skill").click();
    cy.getBySel(prefix + "selected-skill-name").contains(name).click();
  }

  function selectTimeHorizon(name: string) {
    cy.getBySel(prefix + "select-time-horizon").click({force: true});
    cy.getBySel(prefix + "selected-time-horizon-name").contains(name).click({force: true});
  }

  function selectResourceDialogRow(index: number) {
    // select row
    cy.getBySel(prefix + "skill-resource-dialog-module-item-row").eq(index).within(() => {
      cy.getBySel(prefix + "skill-resource-dialog-module-item-checkbox").click();
    });
  }

  function saveResourceDialogAndAssert(index: number, resourceName: string,
                                       resourceItemName: string) {

    // click save
    cy.getBySel(prefix + "skill-resource-dialog-save").click();

    // assert mission objectives in correct state
    cy.getBySel(prefix + "mission-objective-resource-name").eq(index)
    .contains("a", new RegExp(`\^${resourceName}$`));

    cy.getBySel(prefix + "mission-objective-resource-item-name").eq(0)
    .contains("a", new RegExp(`\^${resourceItemName}$`));
  }

});
