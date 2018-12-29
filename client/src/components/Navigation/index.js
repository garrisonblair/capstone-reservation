import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import { Dropdown, Menu } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import Login from '../Login';
import api from '../../utils/api';


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
    const { showLogin } = this.state;

    return (
      <Menu inverted fixed="top">
        <Menu.Item>
          Capstone
        </Menu.Item>
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

export default withRouter(Navigation);
