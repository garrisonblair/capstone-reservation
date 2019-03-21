/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable max-len */
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
import api from '../../../../utils/api';
import ByProgramChart from './ByProgramChart';
import ByGradLevelChart from './ByGradLevelChart';
import ByCategoryChart from './ByCategoryChart';
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
          <Checkbox label="Category" checked={withCategories} onChange={() => this.handleCheckboxChange('withCategories')} />
        </Form.Field>
      </Form.Group>
    );
  }

  render() {
    const {
      stats,
      selected,
      withProgram,
      withGradLevel,
      withCategories,
    } = this.state;

    return (
      <div className="room-stats">
        <h1> Program stats </h1>
        {this.renderDateFilter()}
        {this.renderDropDown()}
        {withProgram && stats.program ? <ByProgramChart stats={stats.program} selected={selected} /> : null}
        {withGradLevel && stats.grad_level ? <ByGradLevelChart stats={stats.grad_level} selected={selected} /> : null}
        {withCategories && stats.category ? <ByCategoryChart stats={stats.category} selected={selected} /> : null}
      </div>
    );
  }
}

export default ProgramStats;
