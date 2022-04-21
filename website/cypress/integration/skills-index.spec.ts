import "cypress-localstorage-commands";

const prefix = "skill-index-";

describe("Skills Index Page", () => {

  beforeEach(() => {
    cy.restoreLocalStorage();
  })

  it("should render skills page", () => {
    cy.visit("/skills");

    cy.getBySel(prefix + "skill-name").should('contain', 'Airflow');

    cy.getBySel(prefix + "skill-id")
    .should('have.attr', 'href')
    .should('not.be.empty')
    .and('contain', '/skills/');

    cy.getBySel(prefix + "add-skill").should('contain', 'Add Skill');
  })
});

