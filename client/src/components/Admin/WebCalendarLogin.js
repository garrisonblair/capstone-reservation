import React, {Component} from 'react';
import {Button, Form, Modal, Input, Header} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';


class WebCalendarLogin extends Component {

  state = {
    username: '',
    password: '',
  }

  saveSettings = () => {
    const {username, password} = this.state

    let data = {
      is_webcalendar_backup_active: true,
      webcalendar_username: username,
      webcalendar_password: password
    }

    api.updateAdminSettings(data)
    .then((response) => {
      sweetAlert(
        'Completed',
        'Settings were successfuly saved.',
        'success'
      )
      this.props.onClose();
    })
    .catch((error) => {
      if (error.message.includes('401')) {
        sweetAlert(
          'Autenthication error',
          'The credentials you entered are invalid.',
          'error'
        )
      }
    })
  }

  handlePasswordChange = (e) => {
    this.setState({password: e.target.value})
  }

  handleUsernameChange = (e) => {
    this.setState({username: e.target.value})
  }

  renderCredentialsInputs() {
    return(
      <div>
        <Form.Field>
          <Input
            fluid
            size='small'
            icon='user'
            iconPosition='left'
            placeholder='Username'
            onChange={this.handleUsernameChange}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size='small'
            icon='lock'
            iconPosition='left'
            placeholder='Password'
            type='password'
            onChange={this.handlePasswordChange}
          />
        </Form.Field>
      </div>
    )
  }

  render() {
    return (
      <Modal open={this.props.show} onClose={this.props.onClose}>
        <Header>
          <h1 className="login__container__header__title">
            {'Please enter your Webcalendar credentials'}
          </h1>
        </Header>
        <div className="login__container__main">
          <div className="ui divider"/>
          <div className="login__container__main__form-wrapper">
            {this.renderCredentialsInputs()}
            <Form.Field>
              <Button fluid size='small' icon onClick={this.saveSettings}>
                Confirm
              </Button>
            </Form.Field>
            <div className="ui divider"/>
          </div>
        </div>
      </Modal>
    )
  }
}

export default WebCalendarLogin;
