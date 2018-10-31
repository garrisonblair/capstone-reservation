import React, {Component} from 'react';
import {Loader, Form, Input, Button, Icon, Step, Label} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import CustomFormInput from './CustomFormInput';
import './Verification.scss';


// TODO: Check if user already set its student ID
class Verification extends Component {
  state = {
    password: {
      value: '',
      showErrorMessage: false,
      errorMessageText: ''
    },
    confirmPassword: {
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
    preventSubmit: true,
    firstName: '',
    userId: 0
  }

  componentDidMount() {
    //This props value is for testing.
    if(this.props.showFormForTesting){
      this.setState({isLoading:false})
    }
    const {token} = this.props.match.params;
    if (token) {
      api.verify(token)
      .then((response) => {
        this.setState({
          isLoading: false,
          firstName: response.data.first_name,
          userId: response.data.id
        });
        localStorage.setItem('CapstoneReservationUser', JSON.stringify(response.data));
      })
      .catch((error) => {
        sweetAlert(
          ":(",
          "something happened",
          "error"
        )
      })
    }
  }

  handleChangepassword = (event) => {
    this.setState({
      password: {
        showErrorMessage: false,
        errorMessageText: '',
        value: event.target.value
      }
    })
  }

  handleChangeConfirmPassword = (event) => {
    this.setState({
      confirmPassword: {
        showErrorMessage: false,
        errorMessageText: '',
        value: event.target.value
      }
    })
  }

  verifyPasswords() {
    const value1 = this.state.password.value;
    const value2 = this.state.confirmPassword.value;

    if (value1 === '') {
      this.setState({
        password: {
          showErrorMessage: true,
          errorMessageText: 'Please enter a password'
        }
      });
      throw new Error();
    }
    if (value2 === '') {
      this.setState({
        confirmPassword: {
          showErrorMessage: true,
          errorMessageText: 'Please re-enter the password'
        }
      });
      throw new Error();
    }
    if (value1 !== value2) {
      this.setState({
        password: {
          showErrorMessage: true,
          errorMessageText: 'Passwords do not match'
        },
        confirmPassword: {
          showErrorMessage: true,
          errorMessageText: 'Passwords do not match'
        },
      })
      throw new Error();
    }
  }

  handleChangeStudentId = (event) => {
    let value = event.target.value;
    let preventSubmit = false;
    let showErrorMessage = false;
    let errorMessageText = '';

    if (value.length === 0) {
      preventSubmit = true;
      showErrorMessage = true;
      errorMessageText = 'Please enter your student ID number';
    } else if (value.length !== 8) {
      preventSubmit = true;
      showErrorMessage = true;
      errorMessageText = 'Field should have 8 digits';
    } else if (!value.match('^[0-9]*$')) {
      preventSubmit = true;
      showErrorMessage = true;
      errorMessageText = 'Student ID should have only digits';
    }

    this.setState({
      preventSubmit,
      studentId: {
        value,
        showErrorMessage,
        errorMessageText,
      }
    })
  }

  handleUserSettings = () => {
    //Verify form before continuing transaction.
    try {
      this.verifyPasswords();
    }
    catch (error) {
      return;
    }

    let {studentId, userId, preventSubmit} = this.state;

    if (preventSubmit) {
      return;
    }

    const password = this.state.password.value;
    const data = {
      "student_id": `${studentId.value}`,
      "password": `${password}`
    }

    api.updateUser(userId, data)
    .then((response) => {
      sweetAlert(
        "Settings",
        "Settings recorded successfuly",
        'success'
      )
      this.props.history.push('/');
    })
    .catch((error) => {
      sweetAlert(
        ":(",
        "There was an error.",
        "error"
      )
    })
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

  renderLoader() {
    return (
      <div>
        <Loader active inline='centered' size="large" />
      </div>
    )
  }

  renderMainForm() {
    let {password, confirmPassword, studentId} = this.state;
    return (
      <div>
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

        <h2>Welcome {this.state.firstName}</h2>
        <Form>
          <Form.Field>
            <label >Enter Password:</label>
            {this.renderInputErrorMessage(password)}
            <Input
              fluid
              size='medium'
              icon='key'
              iconPosition='left'
              type="password"
              onChange={this.handleChangepassword}
            />
          </Form.Field>

          <Form.Field>
            <label>Confirm Password:</label>
            {this.renderInputErrorMessage(confirmPassword)}
            <Input
              fluid
              size='medium'
              icon='key'
              type="password"
              iconPosition='left'
              onChange={this.handleChangeConfirmPassword}
            />
          </Form.Field>

          <CustomFormInput
            fluid
            size='medium'
            icon='id card'
            iconPosition='left'
            placeholder='12345678'
            onChange={this.handleChangeStudentId}
            errormessage={studentId.errorMessageText}
          />
        </Form>
        <Form.Field>
          <br/>
          <Button fluid size='small' icon onClick={this.handleUserSettings}>
            Set settings
          </Button>
        </Form.Field>
      </div>
    )
  }

  render() {
    return (
      <div id="verification">
        <div className="container">
          {this.state.isLoading ? this.renderLoader() : this.renderMainForm()}
        </div>
      </div>
    )
  }
}

export default Verification;
