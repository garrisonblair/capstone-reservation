/* eslint-disable react/prop-types */
import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import {
  Button,
  Form,
  Input,
  Modal,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './Login.scss';


class LoginComponent extends Component {
  state = {
    username: '',
    password: '',
  }

  handleUsernameChange = (event) => {
    this.setState({ username: event.target.value });
  }

  handlePasswordChange = (event) => {
    this.setState({ password: event.target.value });
  }

  handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      this.handleLogin();
    }
  }

  handleLogin = () => {
    // eslint-disable-next-line react/prop-types
    const { username, password } = this.state;

    api.login(username, password)
      .then(response => response.data)
      .then((data) => {
        localStorage.setItem('CapstoneReservationUser', JSON.stringify(data));
        sweetAlert.fire({
          position: 'top',
          type: 'success',
          title: 'Logged in',
          toast: true,
          showConfirmButton: false,
          timer: 2000,
        });
      })
      .catch(() => {
        sweetAlert.fire({
          position: 'top',
          type: 'error',
          text: 'Invalid credentials',
        });
      });
  }

  render() {
    return (
      <Modal.Description className="login__container__main__form-wrapper">
        {/* <Form onSubmit={this.handleLogin}> */}
        <p className="info-text">
          This is not your ENCS password. If you have not already, you need to register.
        </p>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="user"
            iconPosition="left"
            placeholder="Username"
            onChange={this.handleUsernameChange}
            onKeyPress={this.handleKeyPress}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="lock"
            iconPosition="left"
            placeholder="Password"
            type="password"
            onChange={this.handlePasswordChange}
            onKeyPress={this.handleKeyPress}
          />
        </Form.Field>
        <Form.Field>
          <Link to="/resetPassword">Forgot your password?</Link>
        </Form.Field>
        <Form.Field>
          <Button fluid size="small" icon onClick={this.handleLogin}>
            Login
          </Button>
        </Form.Field>
        {/* </Form> */}
        <Form.Field>
          {/* <Link className="ui button" to="/registration">Register?</Link> */}
          <Button fluid size="small" onClick={() => { const { history } = this.props; history.push('/registration'); }}> Register </Button>
        </Form.Field>
        <div className="ui divider" />
      </Modal.Description>
    );
  }
}

export default withRouter(LoginComponent);
