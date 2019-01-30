/* eslint-disable react/no-unused-state */
/* eslint-disable react/prop-types */
/* eslint-disable no-console */
/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import { Bar } from 'react-chartjs-2';

class RoomStats extends Component {
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
    return (
      <div>
        <h1> Room stats </h1>
        {this.renderChart('Hours Booked', 'hours_booked')}
        {this.renderChart('Number of Room Bookings', 'num_room_bookings')}
        {this.renderChart('Average Time Booked Per Day', 'average_time_booked_per_day')}
        {this.renderChart('Average Bookings Per Day', 'average_bookings_per_day')}
      </div>
    );
  }
}

export default RoomStats;
