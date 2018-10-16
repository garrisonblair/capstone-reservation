import axios from 'axios';
import settings from '../../config/settings';
import React, {Component} from 'react';
import './Verification.scss';
import {Loader, Form, Input, Button, Icon, Step, Label} from 'semantic-ui-react'

class Verification extends Component {
  state = {
    password1: {
      value: '',
      showErrorMessage: false,
      errorMessageText: ''
    },
    password2: {
      value: '',
      showErrorMessage: false,
      errorMessageText: ''
    },
    studentId: {
      value: '',
      showErrorMessage: false,
      errorMessageText: ''
    },
    isLoading: true,
    firstName: ''
  }
  componentWillMount() {
    const {token} = this.props.match.params;
    console.log(token);
    if (token) {
      const data = {"token": `${token}`}
      axios({
        method: 'POST',
        url: `${settings.API_ROOT}/verify`,
        data: data
      })
        .then((response) => {
          this.setState({
            isLoading: false,
            firstName: response.data.first_name
          });
          console.log(response);
        })
        .catch((error) => {
          console.log('verification failed')
        })
    }
  }
  handleChangePassword1 = (event) => {
    this.setState({
      password1: {
        showErrorMessage: false,
        errorMessageText: '',
        value: event.target.value
      }
    })
  }
  handleChangePassword2 = (event) => {
    this.setState({
      password2: {
        showErrorMessage: false,
        errorMessageText: '',
        value: event.target.value
      }
    })
  }

  verifyPasswords() {
    const value1 = this.state.password1.value;
    const value2 = this.state.password2.value;

    if (value1 === '') {
      this.setState({
        password1: {
          showErrorMessage: true,
          errorMessageText: 'Please enter a password'
        }
      });
      throw new Error();
    }
    if (value2 === '') {
      this.setState({
        password2: {
          showErrorMessage: true,
          errorMessageText: 'Please re-enter the password'
        }
      });
      throw new Error();
    }
    if (value1 !== value2) {
      this.setState({
        password1: {
          showErrorMessage: true,
          errorMessageText: 'This passwords do not match each other'
        },
        password2: {
          showErrorMessage: true,
          errorMessageText: 'This passwords do not match each other'
        },
      })
      throw new Error();
    }
  }

  verifyStudentId() {
    const {studentId} = this.state;
    console.log('clicked');

    if (studentId.value.length === 0) {
      this.setState({
        studentId: {
          showErrorMessage: true,
          errorMessageText: 'Please enter your student Id number'
        }
      })
      throw new Error();
    }
    if (studentId.value.length !== 8) {
      this.setState({
        studentId: {
          showErrorMessage: true,
          errorMessageText: 'Field should have 8 digits'
        }
      })
      throw new Error();
    }
  }

  handleChangeStudentId = (event) => {
    this.setState({
      studentId: {
        value: event.target.value,
        showErrorMessage: false,
        errorMessageText: ''
      }
    })
  }

  handleUserSettings = () => {
    try {
      this.verifyPasswords();
      this.verifyStudentId();
    }
    catch (error) {
      return;
    }
  }
  renderInputErrorMessage(input) {
    if (input.showErrorMessage) {
      return (
        <div>
          <Label color="red" pointing='below'>{input.errorMessageText}</Label>
        </div>
      )
    }
  }

  render() {
    let {password1, password2, studentId} = this.state;
    return (
      <div id="verification">
        <div className="container">
          <Loader active inline='centered' active={this.state.isLoading} />
          <h1> Account settings </h1>
          <Step.Group size="mini" widths={2}>
            <Step completed>
              <Icon name="envelope" />
              <Step.Content>
                <Step.Title>Step 1</Step.Title>
                <Step.Description>ENCS username verification</Step.Description>
              </Step.Content>
            </Step>
            <Step active>
              <Icon name="cog" />
              <Step.Content>
                <Step.Title>Step 2</Step.Title>
                <Step.Description>Account setup</Step.Description>
              </Step.Content>
            </Step>
          </Step.Group>

          <h4>Welcome {this.state.firstName}</h4>
          <Form>
            <label >Enter Password:</label>
            <Form.Field>
              {this.renderInputErrorMessage(password1)}
              <Input
                fluid
                size='medium'
                icon='key'
                iconPosition='left'
                type="password"
                onChange={this.handleChangePassword1}
              />
            </Form.Field>
            <label>Re-enter password:</label>
            <Form.Field>
              {this.renderInputErrorMessage(password2)}
              <Input
                fluid
                size='medium'
                icon='key'
                type="password"
                iconPosition='left'
                onChange={this.handleChangePassword2}
              />
            </Form.Field>

            <label>Student ID:</label>
            <Form.Field>
              {this.renderInputErrorMessage(studentId)}
              <Input
                fluid
                size='medium'
                icon='id card'
                iconPosition='left'
                placeholder='12345678'
                onChange={this.handleChangeStudentId}
              />
            </Form.Field>
          </Form>

          <Form.Field>
            <br />
            <Button fluid size='small' icon onClick={this.handleUserSettings}>
              Send Email
      </Button>
          </Form.Field>

        </div>

      </div>
    )
  }
}

export default Verification;
