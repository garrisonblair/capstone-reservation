/* eslint-disable array-callback-return */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Bar } from 'react-chartjs-2';
import '../RoomStats.scss';


class ByCategoryChart extends Component {
  renderChart = (header, type) => {
    const { stats } = this.props;
    if (stats.length === 0) {
      return [];
    }

    const labels = [];
    const values = [];
    Object.keys(stats).map((key) => {
      labels.push(key);
      values.push(stats[key][type]);
    });

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
    const { selected } = this.props;
    return (
      <div className="room-stats">
        <h2> By Category </h2>
        {selected.includes('Hours Booked') ? this.renderChart('Hours Booked', 'hours_booked') : ''}
        {selected.includes('Number of Room Bookings') ? this.renderChart('Number of Program Bookings', 'num_bookings') : ''}
      </div>
    );
  }
}

ByCategoryChart.propTypes = {
  stats: PropTypes.shape(Object).isRequired,
  selected: PropTypes.arrayOf(String).isRequired,
};

export default ByCategoryChart;
