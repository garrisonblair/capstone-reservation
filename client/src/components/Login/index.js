import React, {Component} from 'react';
import axios from 'axios';
import {Button, Form, Icon, Input} from 'semantic-ui-react';
import SweetAlert from 'sweetalert2-react';
import settings from '../../config/settings';
import {getTokenHeader} from '../../utils/requestHeaders';
import './Login.scss';


class Login extends Component {

  state = {
    showModal: false,
    modalTitle: '',
    modalText: '',
    modalType: 'success'
  }

  closeModal = () => {
    this.setState({
      showModal: false
    })
  }

  handleUsernameChange = (event) => {
    this.setState({username: event.target.value})
  }

  handlePasswordChange = (event) => {
    this.setState({password: event.target.value})
  }

  handleLogin = () => {
    const {history} = this.props;
    const {username, password} = this.state;
    let data = {
      username,
      password
    }
    axios({
      method: 'POST',
      url: `${settings.API_ROOT}/login`,
      data: data
    })
    .then((response) =>
      response.data
    )
    .then((data) => {
      localStorage.setItem('CapstoneReservationUser', JSON.stringify(data));
      history.push('/');
    })
    .catch((error) => {
      console.log("ERROR");
      this.setState({
        showModal: true,
        modalType: 'error',
        modalTitle: ':(',
        modalText: 'Invalid credentials'
      })
    })
  }

  componentDidMount = () => {
    document.title = 'Login'
  }

  render = () => {
    const {showModal, modalType, modalTitle, modalText} = this.state;
    return (
      <div className="login login--center">
        <div className="login__container">
          <div className="login__container__header">
            <h1 className="login__container__header__title"> Login </h1>
          </div>
          <div className="login__container__main">
            <div className="ui divider"/>
            <div className="login__container__main__form-wrapper">
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
              <Form.Field>
                <Button fluid size='small' icon onClick={this.handleLogin}>
                  Login
                </Button>
              </Form.Field>
              <SweetAlert
                show={showModal}
                title={modalTitle}
                text={modalText}
                type={modalType}
                onConfirm={this.closeModal}
              />
              <div className="ui divider"/>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Login;
