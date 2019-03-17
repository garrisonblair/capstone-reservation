/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
import React, { Component } from 'react';
import {
  Button,
  Checkbox,
  Dropdown,
  Form,
  Icon,
  Input,
  Segment,
} from 'semantic-ui-react';
import { SingleDatePicker } from 'react-dates';
// import * as moment from 'moment';
import { Bar } from 'react-chartjs-2';
import api from '../../../../utils/api';
import ByProgramStats from './ByProgramStats';
import ByGradLevelStats from './ByGradLevelStats';
import 'react-dates/lib/css/_datepicker.css';
import '../RoomStats.scss';


class ProgramStats extends Component {
  state = {
    stats: [],
    selected: ['Hours Booked'],
    date: null,
    focused: false,
    focusStartDate: false,
    focusEndDate: false,
    startDate: '',
    endDate: '',
    withProgram: false,
    withGradLevel: false,
    withCategories: false,
  }

  componentDidMount() {
    this.getStats();
  }

  getStats = () => {
    const {
      startDate, endDate,
      withProgram, withGradLevel, withCategories,
    } = this.state;
    api.getProgramStatistics(startDate, endDate, withProgram, withGradLevel, withCategories)
      .then((response) => {
        const { data: stats } = response;
        this.setState({ stats });
      });
  }

  handleChangeDate = (date) => {
    const { focusStartDate, focusEndDate } = this.state;
    let { startDate, endDate } = this.state;

    if (focusStartDate === true) {
      startDate = date.format('YYYY-MM-DD');
    }

    if (focusEndDate === true) {
      endDate = date.format('YYYY-MM-DD');
    }

    this.setState({
      // date,
      startDate,
      endDate,
    });
  }

  handleDatePickerFocusChange = (f) => {
    let focusStartDate = true;
    let focusEndDate = true;
    if (f === false) {
      focusStartDate = false;
      focusEndDate = false;
    }
    this.setState({
      focusStartDate,
      focusEndDate,
      focused: f,
    });
  }

  handleCheckboxChange = (name) => {
    const { [name]: flag } = this.state;
    this.setState({ [name]: !flag }, () => { this.getStats(); });
  }

  onDropDownChange = (event, data) => {
    this.setState({
      selected: data.value,
    });
  }

  renderDropDown = () => {
    const { selected } = this.state;
    const options = ['Hours Booked', 'Number of Room Bookings', 'Average Time Booked Per Day', 'Average Bookings Per Day'];
    const stateOptions = options.map(option => ({ key: option, value: option, text: option }));
    return (
      <Dropdown
        placeholder="Stats"
        fluid
        multiple
        search
        selection
        value={selected}
        options={stateOptions}
        onChange={this.onDropDownChange}
      />
    );
  }

  renderDateFilter = () => {
    const {
      date,
      focused,
      focusStartDate,
      focusEndDate,
      startDate,
      endDate,
    } = this.state;

    return (
      <Segment>
        <Form>
          <Form.Group>
            <Form.Field>
              <label>from</label>
              <Input
                icon="calendar alternate"
                iconPosition="left"
                placeholder="Start Date"
                focus={focusStartDate}
                value={startDate}
                onClick={() => this.setState({ focusStartDate: true, focused: true })}
                onChange={e => this.setState({ startDate: e.target.value })}
              />
            </Form.Field>
            <Form.Field>
              <label>to</label>
              <Input
                icon="calendar alternate outline"
                iconPosition="left"
                placeholder="End Date"
                focus={focusEndDate}
                value={endDate}
                onClick={() => this.setState({ focusEndDate: true, focused: true })}
                onChange={e => this.setState({ endDate: e.target.value })}
              />
            </Form.Field>
          </Form.Group>
          {this.renderFlags()}
          <SingleDatePicker
            isOutsideRange={() => false}
            numberOfMonths={1}
            date={date}
            onDateChange={d => this.handleChangeDate(d)}
            focused={focused}
            onFocusChange={({ focused: f }) => this.handleDatePickerFocusChange(f)}
            hideKeyboardShortcutsPanel
            id="roomstats-picker"
          />
          <Button onClick={this.getStats}>
            <Icon name="options" />
            Filter
          </Button>
        </Form>
      </Segment>
    );
  }

  renderFlags = () => {
    const { withProgram, withGradLevel, withCategories } = this.state;
    return (
      <Form.Group>
        <Form.Field>
          <Checkbox label="Program" checked={withProgram} onChange={() => this.handleCheckboxChange('withProgram')} />
        </Form.Field>
        <Form.Field>
          <Checkbox label="Grad Level" checked={withGradLevel} onChange={() => this.handleCheckboxChange('withGradLevel')} />
        </Form.Field>
        <Form.Field>
          <Checkbox label="Categories" checked={withCategories} onChange={() => this.handleCheckboxChange('withCategories')} />
        </Form.Field>
      </Form.Group>
    );
  }

  renderChart = (header, type) => {
    const { stats } = this.state;
    if (stats.length === 0) {
      return [];
    }
    const labels = stats.map(stat => stat.program.program);
    const values = stats.map(stat => stat.program[type]);
    const data = {
      labels,
      datasets: [
        {
          label: header,
          backgroundColor: 'rgba(255,99,132,0.2)',
          borderColor: 'rgba(255,99,132,1)',
          borderWidth: 1,
          hoverBackgroundColor: 'rgba(255,99,132,0.4)',
          hoverBorderColor: 'rgba(255,99,132,1)',
          data: values,
        },
      ],
    };

    return (
      <Bar
        data={data}
        width={100}
        height={30}
      />
    );
  }

  renderGradLevelStats() {
    const { selected } = this.state;

    return (
      <div className="room-stats">
        <h2> Graduate Level stats </h2>
        {selected.includes('Hours Booked') ? this.renderChart('Hours Booked', 'hours_booked') : ''}
        {selected.includes('Number of Room Bookings') ? this.renderChart('Number of Program Bookings', 'num_bookings') : ''}
        {selected.includes('Average Time Booked Per Day') ? this.renderChart('Average Time Booked Per Day', 'average_time_booked_per_day') : ''}
        {selected.includes('Average Bookings Per Day') ? this.renderChart('Average Bookings Per Day', 'average_bookings_per_day') : ''}
      </div>
    );
  }

  renderCategoryStats() {
    const { selected } = this.state;

    return (
      <div className="room-stats">
        <h2> Category stats </h2>
        {selected.includes('Hours Booked') ? this.renderChart('Hours Booked', 'hours_booked') : ''}
        {selected.includes('Number of Room Bookings') ? this.renderChart('Number of Program Bookings', 'num_bookings') : ''}
      </div>
    );
  }

  render() {
    const {
      stats,
      selected,
      withProgram,
      withGradLevel,
      // withCategories,
    } = this.state;

    return (
      <div className="room-stats">
        <h1> Program stats </h1>
        {this.renderDateFilter()}
        {this.renderDropDown()}
        {withProgram && stats.program ? <ByProgramStats stats={stats.program} selected={selected} /> : null}
        {withGradLevel && stats.grad_level ? <ByGradLevelStats stats={stats.grad_level} selected={selected} /> : null}
        {/* {withCategories ? this.renderCategoryStats() : null} */}
      </div>
    );
  }
}

export default ProgramStats;
