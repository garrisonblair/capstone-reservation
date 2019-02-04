/* eslint-disable react/no-unused-state */
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
import storage from '../../utils/local-storage';
import './Navigation.scss';


class Navigation extends Component {
  state = {
    showLogin: false,
    update: false,
  }

  static getDerivedStateFromProps(props, state) {
    if (props.update !== state.update) {
      return {
        update: props.update,
      };
    }
    return null;
  }

  handleClickLogo = () => {
    // eslint-disable-next-line react/prop-types
    const { history } = this.props;

    if (history.location.pathname === '/') {
      window.location.reload();
    } else {
      history.push('/');
    }
  }

  handleLogin = () => {
    // eslint-disable-next-line react/prop-types
    const { history } = this.props;
    if (storage.getUser()) {
      api.logout()
        .then(() => {
          sweetAlert.fire({
            position: 'top',
            type: 'success',
            title: 'Logged out',
          });
          this.setState({ showLogin: false });
          if (history.location.pathname !== '/') {
            history.push('/');
          }
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
    if (!storage.getUser()) {
      return '';
    }

    const user = storage.getUser();
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

  renderAccountDropDown = () => {
    if (!localStorage.CapstoneReservationUser) {
      return '';
    }
    // eslint-disable-next-line react/prop-types
    const { history } = this.props;
    const component = (
      <Dropdown item text="Account">
        <Dropdown.Menu>
          <Dropdown.Item icon="user" text="Profile" onClick={() => history.push('profile')} />
          {/* <Dropdown.Item icon="cog" text="Settings" /> */}
        </Dropdown.Menu>
      </Dropdown>
    );

    return component;
  }

  renderLoggedInInfo = () => {
    if (!storage.getUser()) {
      return '';
    }

    const user = storage.getUser();
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
          <Menu.Item className="navigation__title" onClick={this.handleClickLogo}>
            Capstone
          </Menu.Item>
          <Menu.Item>
            <a href="https://docs.google.com/forms/u/1/d/1g-d02gd4s1JQjEEArGkwZVmlYcBeWlDL6M3R2dcFmY8/edit?usp=sharing">Feedback</a>
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
            {this.renderAccountDropDown()}
            <Menu.Item
              onClick={this.handleLogin}
              className="navigation__login"
            >
              {storage.getUser() ? 'Logout' : 'Login'}
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
