import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Dropdown } from 'semantic-ui-react';
import { Bar } from 'react-chartjs-2';

class RoomStats extends Component {
  state = {
    selected: ['Hours Booked'],
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

  renderChart = (header, type) => {
    const { stats } = this.props;
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
      <div>
        <h1> Room stats </h1>
        {this.renderDropDown()}
        {selected.includes('Hours Booked') ? this.renderChart('Hours Booked', 'hours_booked') : ''}
        {selected.includes('Number of Room Bookings') ? this.renderChart('Number of Room Bookings', 'num_room_bookings') : ''}
        {selected.includes('Average Time Booked Per Day') ? this.renderChart('Average Time Booked Per Day', 'average_time_booked_per_day') : ''}
        {selected.includes('Average Bookings Per Day') ? this.renderChart('Average Bookings Per Day', 'average_bookings_per_day') : ''}
      </div>
    );
  }
}

RoomStats.propTypes = {
  stats: PropTypes.instanceOf(Object).isRequired,
};

export default RoomStats;
