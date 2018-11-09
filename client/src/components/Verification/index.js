import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Loader, Form, Button, Icon, Step} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import CustomFormInput from './CustomFormInput';
import './Verification.scss';


// TODO: Check if user already set its booker ID
class Verification extends Component {
  state = {
    password: '',
    confirmPassword: '',
    bookerID: '',
    errorMessagePassword: '',
    errorMessageConfirmPassword: '',
    errorMessageBookerID: '',
    isLoading: true,
    preventSubmit: true,
    firstName: '',
    userId: 0
  }

  verifyPasswords() {
    const {password, confirmPassword} = this.state;
    let preventSubmit = false;
    let errorMessagePassword = '';
    let errorMessageConfirmPassword = '';

    if (password.length === 0) {
      preventSubmit = true;
      errorMessagePassword = 'Please enter a password'
    }

    if (confirmPassword.length === 0) {
      preventSubmit = true;
      errorMessageConfirmPassword = 'Please re-enter the password'
    }

    if (password !== confirmPassword) {
      preventSubmit = true;
      errorMessagePassword = 'Passwords do not match',
      errorMessageConfirmPassword = 'Passwords do not match'
    }

    this.setState({
      preventSubmit,
      errorMessagePassword,
      errorMessageConfirmPassword
    })
  }

  verifyBookerID() {
    let value = this.state.bookerID;
    let preventSubmit = false;
    let errorMessageBookerID = '';

    if (value.length === 0) {
      preventSubmit = true;
      errorMessageBookerID = 'Please enter your booker ID number';
    } else if (value.length !== 8) {
      preventSubmit = true;
      errorMessageBookerID = 'Field should have 8 digits';
    } else if (!value.match('^[0-9]*$')) {
      preventSubmit = true;
      errorMessageBookerID = 'Booker ID should have only digits';
    }

    this.setState({
      preventSubmit,
      bookerID: value,
      errorMessageBookerID
    });
  }

  handleChangePassword = (event) => {
    this.setState({
      password: event.target.value,
      errorMessagePassword: ''
    })
  }

  handleChangeConfirmPassword = (event) => {
    this.setState({
      confirmPassword: event.target.value,
      errorMessageConfirmPassword: ''
    })
  }

  handleChangeBookerId = (event) => {
    this.setState({
      bookerID: event.target.value,
      errorMessageBookerID: ''
    });
  }

  handleSubmit = () => {
    const {bookerID, userId, password, preventSubmit} = this.state;

    // Verify form before continuing transaction.
    this.verifyPasswords();
    this.verifyBookerID();

    if (preventSubmit) {
      return;
    }

    const data = {
      "booker_id": `${bookerID}`,
      "password": `${password}`
    }

    api.updateUser(userId, data)
    .then((response) => {
      sweetAlert(
        "Settings",
        "Settings recorded successfuly",
        'success'
      )
      .then(() => {
        this.props.history.push('/');
      })
    })
    .catch((error) => {
      sweetAlert(
        ":(",
        "There was an error.",
        "error"
      )
    })
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

  renderLoader() {
    return (
      <div>
        <Loader active inline='centered' size="large" />
      </div>
    )
  }

  renderMainForm() {
    let {errorMessagePassword, errorMessageConfirmPassword, errorMessageBookerID} = this.state;
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
          <CustomFormInput
            fluid
            size='medium'
            icon='key'
            type="password"
            iconPosition='left'
            title={`Enter Password:`}
            onChange={this.handleChangePassword}
            errormessage={errorMessagePassword}
          />

          <CustomFormInput
            fluid
            size='medium'
            icon='key'
            type="password"
            iconPosition='left'
            title={`Confirm Password:`}
            onChange={this.handleChangeConfirmPassword}
            errormessage={errorMessageConfirmPassword}
          />

          <CustomFormInput
            fluid
            size='medium'
            icon='id card'
            iconPosition='left'
            placeholder='12345678'
            onChange={this.handleChangeBookerId}
            title={`booker ID:`}
            errormessage={errorMessageBookerID}
          />
        </Form>
        <Form.Field>
          <br/>
          <Button fluid size='small' icon onClick={this.handleSubmit}>
            Save
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

Verification.propTypes = {
  showFormForTesting: PropTypes.bool
}

export default Verification;
