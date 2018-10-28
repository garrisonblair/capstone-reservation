import React, {Component} from 'react';
import settings from '../../config/settings';
import axios from 'axios';
import './Admin.scss';


class Admin extends Component {

  state = {
    isAdmin: false
  }

  componentDidMount = () => {
    document.title = 'Capstone Settings'
    if(localStorage.getItem('CapstoneReservationUser')) {
      let user = JSON.parse(localStorage.getItem('CapstoneReservationUser'));
      if(user.is_superuser) {
        this.setState({
          isAdmin: true,
          current: 'Settings'
        })
        this.getSettings()
      }
    }
  }

  /************ REQUESTS *************/

  //TODO: Put correct url and handle response
  getSettings() {
    // axios({
    //   method: 'GET',
    //   url: `${settings.API_ROOT}/settings`
    // })
    // .then((response) => {

    // })
    // .catch(function (error) {
    //   console.log(error);
    // })
    // .then(function () {
    //   // always executed
    // });
  }

  /************ CLICK HANDLING METHODS *************/

  handleClickNav = (e) => {
    let option = e.target.getAttribute('value');
    this.setState({current: option})
  }


  /************ COMPONENT RENDERING *************/

  renderSettings() {
    if(this.state.isAdmin) {
      return <div className="admin__wrapper"> <div>{this.renderNav()}</div><div>{this.renderContent()}</div></div>
    } else {
      return <div> NOT FOUNDED </div>
    }
  }

  renderNav() {
    const options = ['Settings', 'Web Calendar', 'Stats']
    const menu = options.map((option) => 
      <li className={this.state.current == option ? "active" : ""} key={option} value={option} onClick={this.handleClickNav}>{option}</li>
    )
    return <ul className="admin__navigation">{menu}</ul>
  }

  renderContent() {
    const {current} = this.state
    let content
    if(current == "Settings") {
      content = <div>Settings</div>
    } else if(current == "Web Calendar") {
      content = <div>Web Calendar</div>
    } else {
      content = <div>Stats</div>
    } 
    return content
    
  }
  

  render() {
    return (
      <div>
        {this.renderSettings()}
      </div>     
    )
  }
}

export default Admin;
