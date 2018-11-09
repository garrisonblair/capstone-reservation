import React from 'react';
import renderer from 'react-test-renderer';
import Enzyme, {shallow} from 'enzyme';
import {HashRouter as Router, Route} from 'react-router-dom';
import PrivilegeCategory from '../../components/Admin/PrivilegeCategory';


it('Shows Privlege Category', () => {
    let privilegesMock = [
        {
            "id": 1,
            "name": "Default",
            "parent_category": '',
            "max_days_until_booking": 7,
            "can_make_recurring_booking": false,
            "max_bookings": 7,
            "max_recurring_bookings": 0,
            "booking_start_time": "08:00:00",
            "booking_end_time": "23:00:00"
        },
        {
            "id": 2,
            "name": "SOEN490",
            "parent_category": 1,
            "max_days_until_booking": 14,
            "can_make_recurring_booking": true,
            "max_bookings": 14,
            "max_recurring_bookings": 52,
            "booking_start_time": "06:00:00",
            "booking_end_time": "23:00:00"
        },
    ];

    const component = (
        <PrivilegeCategory privilegesMock={privilegesMock}/>
    )
    const app = shallow(
        <Router>
            <Route exact path="/admin/privileges" component={component}/>
        </Router>
    );
    const tree = renderer
        .create(app)
        .toJSON();
    expect(tree).toMatchSnapshot();
});
