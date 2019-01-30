/* eslint-disable react/no-unused-state */
/* eslint-disable react/prop-types */
/* eslint-disable no-console */
/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import { Bar } from 'react-chartjs-2';

class RoomStats extends Component {
  renderHoursBooked = () => {
    const { stats } = this.props;
    if (stats.length === 0) {
      return [];
    }
    const labels = stats.map(stat => stat.room.name);
    const values = stats.map(stat => stat.hours_booked);
    const data = {
      labels,
      datasets: [
        {
          label: 'Hours Booked',
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

  renderNumberRoomBookings = () => {
    const { stats } = this.props;
    if (stats.length === 0) {
      return [];
    }
    const labels = stats.map(stat => stat.room.name);
    const values = stats.map(stat => stat.num_room_bookings);
    const data = {
      labels,
      datasets: [
        {
          label: 'Number of Room Bookings',
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

  renderAverageTimeBooked = () => {
    const { stats } = this.props;
    if (stats.length === 0) {
      return [];
    }
    const labels = stats.map(stat => stat.room.name);
    const values = stats.map(stat => stat.average_time_booked_per_day);
    const data = {
      labels,
      datasets: [
        {
          label: 'Average Time Booked Per Day',
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

  renderAverageBookings = () => {
    const { stats } = this.props;
    if (stats.length === 0) {
      return [];
    }
    const labels = stats.map(stat => stat.room.name);
    const values = stats.map(stat => stat.average_bookings_per_day);
    const data = {
      labels,
      datasets: [
        {
          label: 'Average Bookings Per Day',
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
        {this.renderHoursBooked()}
        {this.renderNumberRoomBookings()}
        {this.renderAverageTimeBooked()}
        {this.renderAverageBookings()}
      </div>
    );
  }
}

export default RoomStats;
