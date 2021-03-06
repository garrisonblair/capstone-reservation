import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Icon, Menu } from 'semantic-ui-react';
import { SingleDatePicker } from 'react-dates';
import moment from 'moment';
import './Calendar.scss';
import 'react-dates/lib/css/_datepicker.css';
import './react_dates_overrides.css';


class SelectedDate extends Component {
  state = {
    focusDate: false,
    date: moment(),
  }

  static getDerivedStateFromProps(props, state) {
    if (props.update !== state.update && props.forDisplay) {
      return {
        update: props.update,
        date: moment(),
      };
    }
    return null;
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
    selectedDate.setFullYear(parseInt(d[0], 10), parseInt(d[1], 10) - 1, parseInt(d[2], 10));
    changeDate(selectedDate);
  }

  focusDate = () => {
    const { onOpenDatePicker } = this.props;
    this.setState({ focusDate: true });
    onOpenDatePicker();
  }

  focusOutDate = (f) => {
    const { onCloseDatePicker } = this.props;
    this.setState({ focusDate: f });
    onCloseDatePicker();
  }

  render() {
    const { date, focusDate } = this.state;

    return (
      <Menu.Item position="right" className="menu--date">
        <Icon
          className="arrow"
          circular
          name="angle left"
          onClick={this.handleClickPreviousDate}
        />
        <Icon name="calendar alternate outline" onClick={this.focusDate} />
        <div className="datepicker">
          <SingleDatePicker
            isOutsideRange={() => false}
            numberOfMonths={1}
            date={date}
            onDateChange={d => this.handleChangeDate(d)}
            focused={focusDate}
            onFocusChange={({ f }) => this.focusOutDate(f)}
            hideKeyboardShortcutsPanel
            id="datepicker"
          />
        </div>
        <span onClick={this.focusDate} role="presentation" onKeyDown={() => {}}>{date.format('ddd MMM Do YYYY')}</span>
        <Icon
          className="arrow"
          circular
          name="angle right"
          onClick={this.handleClickNextDate}
        />
      </Menu.Item>
    );
  }
}

SelectedDate.propTypes = {
  changeDate: PropTypes.func,
  onOpenDatePicker: PropTypes.func,
  onCloseDatePicker: PropTypes.func,
};

SelectedDate.defaultProps = {
  changeDate: () => {},
  onOpenDatePicker: () => {},
  onCloseDatePicker: () => {},
};

export default SelectedDate;
