import PropTypes from 'prop-types';
import React, { Component } from 'react';
import './Calendar.scss';
import { Button, Icon } from 'semantic-ui-react';


class SelectedDate extends Component {
  state = {
    selectedDate: new Date(),
  }

  handleClickNextDate = () => {
    const { selectedDate } = this.state;
    selectedDate.setDate(selectedDate.getDate() + 1);
    this.setState({ selectedDate });
    this.changeDate(selectedDate);
  }

  handleClickPreviousDate = () => {
    const { selectedDate } = this.state;
    selectedDate.setDate(selectedDate.getDate() - 1);
    this.setState({ selectedDate });
    this.changeDate(selectedDate);
  }

  changeDate = (day) => {
    const { changeDate } = this.props;
    changeDate(day);
  }

  render() {
    const { selectedDate } = this.state;
    return (
      <div className="calendar__date">
        <div className="calendar__date__header">
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
            {selectedDate.toDateString()}
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
      </div>
    );
  }
}

SelectedDate.propTypes = {
  changeDate: PropTypes.func,
};

SelectedDate.defaultProps = {
  changeDate: () => {},
};

export default SelectedDate;
