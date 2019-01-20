import React, { Component } from 'react';
import './Calendar.scss';


class Hours extends Component {
  state = {
    hoursList: [],
    hoursNum: 0,
    orientation: 0,
  }

  static getDerivedStateFromProps(props, state) {
    if (props.hoursList === state.hoursList && props.orientation === state.orientation) {
      return null;
    }
    return {
      hoursList: props.hoursList,
      hoursNum: props.hoursNum,
      orientation: props.orientation,
    };
  }

  setStyle() {
    const { hoursNum, orientation } = this.state;
    let style;
    if (orientation === 0) {
      style = {
        gridTemplateRows: `repeat(${hoursNum}, 1fr)`,
      };
    } else {
      style = {
        gridTemplateColumns: `repeat(${hoursNum}, 1fr)`,
      };
    }
    return style;
  }


  render() {
    const { hoursList } = this.state;
    const hours = hoursList.map(hour => (
      <div className="calendar__hours__hour" key={hour}>
        {hour}
      </div>
    ));

    return <div className="calendar__hours__wrapper" style={this.setStyle()}>{hours}</div>;
  }
}

export default Hours;
