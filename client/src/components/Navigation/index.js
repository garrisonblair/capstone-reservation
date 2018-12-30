import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import { Dropdown, Menu, Icon } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import { SingleDatePicker } from 'react-dates';
import * as moment from 'moment';
import Login from '../Login';
import api from '../../utils/api';
import './Navigation.scss';


class Navigation extends Component {
  state = {
    showLogin: false,
    focusDate: false,
    date: moment(),
  }

  handleLogin = () => {
    if (localStorage.CapstoneReservationUser) {
      api.logout()
        .then(() => {
          sweetAlert(
            'Logged out',
            '',
            'success',
          );
          this.setState({ showLogin: false });
        });
    } else {
      this.setState({ showLogin: true });
    }
  }

  closeLogin = () => {
    this.setState({ showLogin: false });
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

  // handleItemClick = (e, { name }) => this.setState({ activeItem: name })

  renderAdminSettings = () => {
    if (!localStorage.CapstoneReservationUser) {
      return '';
    }

    const user = JSON.parse(localStorage.CapstoneReservationUser);
    if (!user.is_superuser) {
      return '';
    }

    // eslint-disable-next-line react/prop-types
    const { history } = this.props;
    const component = (
      <Menu.Item onClick={() => { history.push('admin'); }}>
        Admin
      </Menu.Item>
    );

    return component;
  }

  render() {
    const { showLogin, focusDate, date } = this.state;
    const { showDate } = this.props;

    return (
      <Menu inverted fixed="top">
        <Menu.Item>
          Capstone
        </Menu.Item>
        { showDate
          ? (
            <Menu.Item position="right">
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
              {date.format('YYYY-MM-DD')}
            </Menu.Item>
          )
          : null
        }
        <Menu.Menu position="right" inverted="true">
          {this.renderAdminSettings()}
          <Dropdown item text="Account">
            <Dropdown.Menu>
              <Dropdown.Item icon="user" text="Profile" />
              <Dropdown.Item icon="cog" text="Settings" />
            </Dropdown.Menu>
          </Dropdown>
          <Menu.Item
            onClick={this.handleLogin}
          >
            {localStorage.CapstoneReservationUser ? 'Logout' : 'Login'}
          </Menu.Item>
        </Menu.Menu>
        <Login
          show={showLogin}
          onClose={this.closeLogin}
        />
      </Menu>
    );
  }
}

Navigation.propTypes = {
  showDate: PropTypes.bool,
  changeDate: PropTypes.func,
};

Navigation.defaultProps = {
  showDate: false,
  changeDate: () => {},
};

export default withRouter(Navigation);
