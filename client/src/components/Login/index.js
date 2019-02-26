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
import './Login.scss';


class Login extends Component {
  state = {
    username: '',
    password: '',
    show: false,
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.show) {
      this.setState({
        show: nextProps.show,
      });
    }
  }

  closeModal = () => {
    const { onClose } = this.props;
    onClose();
    this.setState({
      show: false,
    });
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
        this.closeModal();
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
    const { show } = this.state;
    return (
      <Modal closeIcon open={show} onClose={this.closeModal} className="login__container" centered={false}>
        <Modal.Header>
          <h1 className="login__container__header__title"> Login </h1>
        </Modal.Header>
        <Modal.Content>
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
        </Modal.Content>
        {/* <div className="login login--center">
          <div className="login__container">
            <div className="login__container__header">
              <h1 className="login__container__header__title"> Login </h1>
            </div>
            <div className="login__container__main">
              <div className="ui divider" />
              <div className="login__container__main__form-wrapper">
                <Form.Field>
                  <Input
                    fluid
                    size="small"
                    icon="user"
                    iconPosition="left"
                    placeholder="Username"
                    onChange={this.handleUsernameChange}
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
                  />
                </Form.Field>
                <Form.Field>
                  <Button fluid size="small" icon onClick={this.handleLogin}>
                    Login
                  </Button>
                </Form.Field>
                <div className="ui divider" />
                <span>
                  First time?
                  <Link to="/registration">Register!</Link>
                </span>
              </div>
            </div>
          </div>
        </div> */}
      </Modal>
    );
  }
}

Login.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func,
};

Login.defaultProps = {
  onClose: () => {
    const { onClose } = this.props;
    onClose();
    this.setState({
      show: false,
    });
  },
};

export default withRouter(Login);
