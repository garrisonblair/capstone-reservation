import PropTypes from 'prop-types';
import React, {Component} from 'react';
import './Calendar.scss';
import {Button, Icon} from 'semantic-ui-react';


class SelectedDate extends Component {

  state = {
    selectedDate: new Date(),
  }

  handleClickNextDate = (e) => {
    let nextDay = this.state.selectedDate;
    nextDay.setDate(nextDay.getDate() + 1);
    this.setState({selectedDate: nextDay})
    this.changeDate(nextDay)
  }

  handleClickPreviousDate = (e) => {
    let previousDay = this.state.selectedDate;
    previousDay.setDate(previousDay.getDate() - 1);
    this.setState({selectedDate: previousDay})
    this.changeDate(previousDay)
  }

  changeDate = (day) => {
    this.props.changeDate(day);
  }

  render() {
    return (
      <div className="calendar__date">
        <Button
          basic
          circular
          color="olive"
          icon="chevron left"
          size="tiny"
          onClick={this.handleClickPreviousDate}
        />
        <h3 className="calendar__date__header">
          <Icon name="calendar alternate outline" />
          {this.state.selectedDate.toDateString()}
        </h3>
        <Button
          basic
          circular
          color="olive"
          icon="chevron right"
          size="tiny"
          onClick={this.handleClickNextDate}
        />
      </div>
    );
  }
}

SelectedDate.propTypes = {
  changeDate: PropTypes.func,
}


export default SelectedDate;
