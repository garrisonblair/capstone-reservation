/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
import React, { Component } from 'react';
import {
  Button,
  Dropdown,
  Form,
  Icon,
  Input,
  Segment,
} from 'semantic-ui-react';
import { SingleDatePicker } from 'react-dates';
import { Bar } from 'react-chartjs-2';
import api from '../../../utils/api';
import 'react-dates/lib/css/_datepicker.css';
import './RoomStats.scss';


class RoomStats extends Component {
  state = {
    stats: [],
    selected: ['Hours Booked'],
    date: null,
    focused: false,
    focusStartDate: false,
    focusEndDate: false,
    startDate: '',
    endDate: '',
  }

  componentDidMount() {
    this.getStats();
  }

  getStats = () => {
    const { startDate, endDate } = this.state;
    api.getRoomStatistics(startDate, endDate)
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

  renderChart = (header, type) => {
    const { stats } = this.state;
    if (stats.length === 0) {
      return [];
    }
    const labels = stats.map(stat => stat.room.name);
    const values = stats.map(stat => stat[type]);
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

  render() {
    const { selected } = this.state;

    return (
      <div className="room-stats">
        <h1> Room stats </h1>
        {this.renderDateFilter()}
        {this.renderDropDown()}
        {selected.includes('Hours Booked') ? this.renderChart('Hours Booked', 'hours_booked') : ''}
        {selected.includes('Number of Room Bookings') ? this.renderChart('Number of Room Bookings', 'num_room_bookings') : ''}
        {selected.includes('Average Time Booked Per Day') ? this.renderChart('Average Time Booked Per Day', 'average_time_booked_per_day') : ''}
        {selected.includes('Average Bookings Per Day') ? this.renderChart('Average Bookings Per Day', 'average_bookings_per_day') : ''}
      </div>
    );
  }
}

export default RoomStats;
