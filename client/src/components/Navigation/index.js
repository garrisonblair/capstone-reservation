import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import {
  Dropdown,
  Menu,
  Icon,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import SelectedDate from '../Calendar/SelectedDate';
import Login from '../Login';
import api from '../../utils/api';
import './Navigation.scss';


class Navigation extends Component {
  state = {
    showLogin: false,
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
    changeDate(date);
  }

  onOpenDatePicker = () => {
    const { onOpenDatePicker } = this.props;
    onOpenDatePicker();
  }

  onCloseDatePicker = () => {
    const { onCloseDatePicker } = this.props;
    onCloseDatePicker();
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
      <Menu.Item onClick={() => { history.push('admin'); }} className="navigation__admin">
        <Icon name="university" />
        Admin
      </Menu.Item>
    );

    return component;
  }

  renderLoggedInInfo = () => {
    if (!localStorage.CapstoneReservationUser) {
      return '';
    }

    const user = JSON.parse(localStorage.CapstoneReservationUser);
    const component = (
      <Menu.Item className="navigation__user">
        <Icon name="user" />
        {`Logged in as ${user.username}`}
      </Menu.Item>
    );
    return component;
  }

  render() {
    const { showLogin } = this.state;
    const { showDate } = this.props;

    return (
      <div className="navigation">
        <Menu inverted fixed="top" className="navigation__bar">
          <Menu.Item className="navigation__title">
            Capstone
          </Menu.Item>
          { showDate
            ? (
              <SelectedDate
                changeDate={this.handleChangeDate}
                onOpenDatePicker={this.onOpenDatePicker}
                onCloseDatePicker={this.onCloseDatePicker}
              />
            )
            : null}
          <Menu.Menu position="right" inverted="true" className="navigation__container">
            {this.renderLoggedInInfo()}
            {this.renderAdminSettings()}
            <Dropdown item text="Account">
              <Dropdown.Menu>
                <Dropdown.Item icon="user" text="Profile" />
                <Dropdown.Item icon="cog" text="Settings" />
              </Dropdown.Menu>
            </Dropdown>
            <Menu.Item onClick={this.handleLogin} className="navigation__login">
              {localStorage.CapstoneReservationUser ? 'Logout' : 'Login'}
            </Menu.Item>
          </Menu.Menu>
          <Login
            show={showLogin}
            onClose={this.closeLogin}
          />
        </Menu>
      </div>
    );
  }
}

Navigation.propTypes = {
  showDate: PropTypes.bool,
  changeDate: PropTypes.func,
  onOpenDatePicker: PropTypes.func,
  onCloseDatePicker: PropTypes.func,
};

Navigation.defaultProps = {
  showDate: false,
  changeDate: () => {},
  onOpenDatePicker: () => {},
  onCloseDatePicker: () => {},
};

export default withRouter(Navigation);
