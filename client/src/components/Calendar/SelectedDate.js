import PropTypes from 'prop-types';
import React, { Component } from 'react';
import './Calendar.scss';
import { Icon, Menu } from 'semantic-ui-react';
import { SingleDatePicker } from 'react-dates';
import * as moment from 'moment';


class SelectedDate extends Component {
  state = {
    focusDate: false,
    date: moment(),
  }

  handleClickNextDate = () => {
    const { date } = this.state;
    this.setState({ date: date.add(1, 'days').calendar() });
    this.handleChangeDate(date);
  }

  handleClickPreviousDate = () => {
    const { date } = this.state;
    this.setState({ date: date.subtract(1, 'days').calendar() });
    this.handleChangeDate(date);
  }

  handleChangeDate = (date) => {
    const { changeDate } = this.props;
    this.setState({ date });
    const d = date.format('YYYY-MM-DD').split('-');
    const selectedDate = new Date();
    selectedDate.setFullYear(parseInt(d[0], 10));
    selectedDate.setMonth(parseInt(d[1], 10) - 1);
    selectedDate.setDate(parseInt(d[2], 10));
    changeDate(selectedDate);
  }

  render() {
    const { date, focusDate } = this.state;
    return (
      <Menu.Item position="right">
        <Icon
          circular
          color="olive"
          name="angle left"
          onClick={this.handleClickPreviousDate}
        />
        <Icon name="calendar alternate outline" onClick={() => this.setState({ focusDate: true })} />
        <div className="datepicker">
          <SingleDatePicker
            isOutsideRange={() => false}
            numberOfMonths={1}
            date={date}
            onDateChange={d => this.handleChangeDate(d)}
            focused={focusDate}
            onFocusChange={({ f }) => this.setState({ focusDate: f })}
            id="datepicker"
          />
        </div>
        <span onClick={() => this.setState({ focusDate: true })} role="presentation" onKeyDown={() => {}}>{date.format('YYYY-MM-DD')}</span>
        <Icon
          circular
          color="olive"
          name="angle right"
          onClick={this.handleClickNextDate}
        />
      </Menu.Item>
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
