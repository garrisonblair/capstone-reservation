import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Form, Modal, Input, Header,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';


class WebCalendarLogin extends Component {
  state = {
    username: '',
    password: '',
  }

  saveSettings = () => {
    const { username, password } = this.state;
    const { onClose } = this.props;
    const data = {
      is_webcalendar_backup_active: true,
      webcalendar_username: username,
      webcalendar_password: password,
    };

    api.updateAdminSettings(data)
      .then(() => {
        sweetAlert(
          'Completed',
          'Settings were successfuly saved.',
          'success',
        );
        onClose();
      })
      .catch((error) => {
        if (error.message.includes('401')) {
          sweetAlert(
            'Autenthication error',
            'The credentials you entered are invalid.',
            'error',
          );
        }
      });
  }

  handlePasswordChange = (e) => {
    this.setState({ password: e.target.value });
  }

  handleUsernameChange = (e) => {
    this.setState({ username: e.target.value });
  }

  renderCredentialsInputs() {
    return (
      <div>
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
      </div>
    );
  }

  render() {
    const { show, onClose } = this.props;
    return (
      <Modal open={show} onClose={onClose}>
        <Header>
          <h1 className="login__container__header__title">
            {'Please enter your Webcalendar credentials'}
          </h1>
        </Header>
        <div className="login__container__main">
          <div className="ui divider" />
          <div className="login__container__main__form-wrapper">
            {this.renderCredentialsInputs()}
            <Form.Field>
              <Button fluid size="small" icon onClick={this.saveSettings}>
                Confirm
              </Button>
            </Form.Field>
            <div className="ui divider" />
          </div>
        </div>
      </Modal>
    );
  }
}


WebCalendarLogin.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default WebCalendarLogin;
