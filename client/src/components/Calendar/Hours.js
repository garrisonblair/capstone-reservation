import PropTypes from 'prop-types';
import React, {Component} from 'react';
import './Calendar.scss';


class Hours extends Component {

  state = {
    hoursList: [],
  }

  static getDerivedStateFromProps(props, state) {
    if(props.hoursList === state.hoursList) {
      return null;
    }
    return {
      hoursList: props.hoursList,
    };
  }

  render() {
    const {hoursList} = this.state;
    const hours = hoursList.map((hour) =>
      <div className="calendar__hours__hour" key={hour}>
        {hour}
      </div>
    );

    return <div className="calendar__hours__wrapper">{hours}</div>
  }
}

Hours.propTypes = {
  hoursList: PropTypes.array,
}


export default Hours;
