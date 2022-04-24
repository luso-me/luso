<script lang="ts">
  import {Cell} from "@smui/layout-grid";
  import Accordion, {Content, Header, Panel} from "@smui-extra/accordion";
  import IconButton, {Icon} from "@smui/icon-button";
</script>

<Cell class="faq-heading text-center" spanDevices={{desktop: 6, tablet: 6, phone: 4}}>
  <hr />
  <h1 class="text-center">Frequently Asked Questions</h1>
</Cell>

<Cell class="faq-items" spanDevices={{desktop: 6, tablet: 4, phone: 4}}>
  <Accordion multiple>
    <Panel>
      <Header>
        <strong>What do you mean by Skill?</strong>
        <IconButton slot="icon" toggle>
          <Icon class="material-icons" on>expand_less</Icon>
          <Icon class="material-icons">expand_more</Icon>
        </IconButton>
      </Header>
      <Content>
        Skill in our world means any tool, practice or process related to IT, past &
        present included. Each Skill is categorized into one of four categories as per
        the wonderful
        <a href="https://www.thoughtworks.com/radar" target="_blank">
          ThoughtWorks Technology Radar.
        </a>
        <br /><br />
        The categories are:
        <li>
          <a href="https://www.thoughtworks.com/radar/techniques" target="_blank">
            Techniques
          </a>
        </li>
        <li>
          <a href="https://www.thoughtworks.com/radar/tools" target="_blank"> Tools </a>
        </li>
        <li>
          <a href="https://www.thoughtworks.com/radar/platforms" target="_blank">
            Platforms
          </a>
        </li>
        <li>
          <a
            href="https://www.thoughtworks.com/radar/languages-and-frameworks"
            target="_blank"
          >
            Languages & Frameworks
          </a>
        </li>
      </Content>
    </Panel>
    <Panel>
      <Header>
        <strong>What do you mean by Skill Resource or Resource?</strong>
        <IconButton slot="icon" toggle>
          <Icon class="material-icons" on>expand_less</Icon>
          <Icon class="material-icons">expand_more</Icon>
        </IconButton>
      </Header>
      <Content>
        A Skill Resource or Resource means any educational resource that contributes to
        helping you learn a particular skill.
        <br /><br />

        For example:
        <li>Books</li>
        <li>Official Documentation</li>
        <li>Online Courses (e.g. Udemy, Coursera, EdX, etc.)</li>
        <li>Tutorials/Blogs/Websites</li>
      </Content>
    </Panel>
    <Panel>
      <Header>
        <strong> Does Luso plan on creating its own Resources? </strong>
        <IconButton slot="icon" toggle>
          <Icon class="material-icons" on>expand_less</Icon>
          <Icon class="material-icons">expand_more</Icon>
        </IconButton>
      </Header>
      <Content>
        No. We believe that there is already a sufficient amount of Educational
        Resources available, for whatever skill you want to learn.
        <br /><br />
        One of our core functions is to act as a Resource aggregator & verifier.
      </Content>
    </Panel>
    <Panel>
      <Header>
        <strong>Why Luso.me?</strong>
        <IconButton slot="icon" toggle>
          <Icon class="material-icons" on>expand_less</Icon>
          <Icon class="material-icons">expand_more</Icon>
        </IconButton>
      </Header>
      <Content>
        Luso means <strong>Skill</strong> in
        <a href="https://en.wikipedia.org/wiki/Chewa_language" target="_blank">
          Chewa.
        </a>
        Literal translation, Skill Me &#128640;
      </Content>
    </Panel>
  </Accordion>
</Cell>
