<script lang="ts">
  import Button, {Icon, Label} from "@smui/button";
  import {goto} from "@roxi/routify";
  import Select, {Option} from "@smui/select";
  import FullCalendar, {PluginDef} from "svelte-fullcalendar";
  import dayGridPlugin from "@fullcalendar/daygrid";
  import timeGridPlugin from "@fullcalendar/timegrid";
  import interactionPlugin from "@fullcalendar/interaction";
  import LayoutGrid, {Cell} from "@smui/layout-grid";
  import FormField from "@smui/form-field";
  import Radio from "@smui/radio";
  import {authStore} from "../../stores";
  import UserService from "../../services/user-service";

  /* FullCalendar */
  let options: {
    droppable: boolean; weekends: boolean; dateClick: (event) => void; editable: boolean;
    plugins: PluginDef[]; headerToolbar: { left: string; center: string; right: string };
    initialView: string; height: string
    events: ({ start: Date; title: string } | { allDay: any; start: string; title: string })[];
  } = {
    dateClick: handleDateClick,
    droppable: true,
    editable: true,
    events: [
      // initial event data
      {title: 'New Event', start: new Date()},
    ],
    initialView: 'dayGridMonth',
    plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay',
    },
    height: '500px',
    weekends: true,
  };
  let calendarComponentRef;
  let eventData = {title: 'my event', duration: '02:00'};

  function toggleWeekends() {
    options.weekends = !options.weekends;
    options = {...options};
  }

  function gotoPast() {
    let calendarApi = calendarComponentRef.getAPI();
    calendarApi.gotoDate('2000-01-01'); // call a method on the Calendar object
  }

  function handleDateClick(event) {
    if (
        confirm('Would you like to add an event to ' + event.dateStr + ' ?')
    ) {
      const {events} = options;
      const calendarEvents = [
        ...events,
        {
          title: 'New Event',
          start: event.date,
          allDay: event.allDay,
        },
      ];
      options = {
        ...options,
        events: calendarEvents,
      };
    }
  }

  let ships = [
    {id: 1, name: "destroyer"},
    {id: 2, name: "fighter"},
    {id: 3, name: "death"}
  ]

  let myship;

  enum ShipType {
    destroyer = "Destroyer",
    fighter = "Fighter",
    death = "Death"
  }

  export let name: string = "Home";
  export let clicked: number = 0;

  /* Radio Button */
  let optionsRadio = [{name: 'Single Skill'}, {name: 'Set of Skills'}];
  let selected = [];

  let id = 100;

  const handleOnClick = event => {
    const name = event.target.name;
    console.log(`clicked name: ${name}`)
  };

  /* Auth */
  function handleAuth() {
    console.log('x : ' + JSON.stringify($authStore.access_token));
    console.log('token : ' + $authStore);
  }

  function handleMe() {
    new UserService().me().then(x => console.log(JSON.stringify(x)));
  }
</script>

<Button on:click={handleMe} variant="raised">
  Handle Auth Me
</Button>

<Button on:click={handleAuth} variant="raised">
  Handle Auth
</Button>

<Button on:click={() => $goto('/auth/github')} variant="raised">
  Auth Me Nav
</Button>

<LayoutGrid>
  <Cell span="{12}">
    What do you want to learn?
    {#each optionsRadio as option}
      <FormField>
        <Radio bind:group={selected} value={option.name} disabled={option.disabled}/>
        <span slot="label">
              {option.name}
            </span>
      </FormField>
    {/each}
  </Cell>
  <Cell span="{12}">
    {#if selected === "Single Skill"}
      Single Skill
      <!--      <UserSkillPlanSingleSkillForm {user} skillId="{null}"/>-->
    {:else}
      Multiple Skill Form
      <!--      <UserSkillPlanMultipleSkillForm/>-->
    {/if}
  </Cell>
</LayoutGrid>

<FullCalendar {options}/>

<Select bind:value={myship} label="Select Ship"
        key={(myship) => (myship && myship.name) || ''}>
  {#each ships as ship}
    <Option value={ship}>{ship.name}</Option>
  {/each}
</Select>

<br/><br/>

{#each Object.entries(ShipType) as ship}
  key: {ship[0]} value: {ship[1]} <br/>
{/each}


<Button on:click={() => clicked++} variant="raised">
  <Icon class="material-icons">thumb_up</Icon>
  <Label>Click Me</Label>
</Button>

<p class="mdc-typography--body1">
  {#if clicked}
    You've clicked the button {clicked} time{clicked === 1 ? "" : "s"}.
  {:else}
    <span class="grayed">You haven't clicked the button.</span>
  {/if}
</p>
