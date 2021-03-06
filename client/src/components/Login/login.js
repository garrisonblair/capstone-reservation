/* eslint-disable react/prop-types */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Link, withRouter } from 'react-router-dom';
import {
  Button,
  Form,
  Input,
  Modal,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
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
    const { onSuccess } = this.props;

    api.login(username, password)
      .then(response => response.data)
      .then((data) => {
        storage.saveUser(data);
        sweetAlert.fire({
          position: 'top',
          type: 'success',
          title: 'Logged in',
          toast: true,
          showConfirmButton: false,
          timer: 2000,
        });
        onSuccess();
        // window.location.reload();
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
        <Form.Field>
          <Button fluid size="small" onClick={() => { const { history } = this.props; history.push('/registration'); }}> Register </Button>
        </Form.Field>
      </Modal.Description>
    );
  }
}

LoginComponent.propTypes = {
  onSuccess: PropTypes.func,
};

LoginComponent.defaultProps = {
  onSuccess: () => {},
};

export default withRouter(LoginComponent);
