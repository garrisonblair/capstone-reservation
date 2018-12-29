import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import { Menu } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import Login from '../Login';
import api from '../../utils/api';


// eslint-disable-next-line react/prefer-stateless-function
class Navigation extends Component {
  state = {
    showLogin: false,
  }

  handleLogin = () => {
    if (localStorage.getItem('CapstoneReservationUser')) {
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

  render() {
    const { showLogin } = this.state;

    return (
      <Menu inverted>
        <Menu.Item>
          Capstone
        </Menu.Item>
        <Menu.Menu position="right" inverted="true">
          <Menu.Item
            onClick={this.handleLogin}
          >
            {localStorage.getItem('CapstoneReservationUser') ? 'Logout' : 'Login'}
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
