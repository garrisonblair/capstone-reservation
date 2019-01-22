import React from 'react';
import renderer from 'react-test-renderer';
import RequestPrivilege from '../../components/Groups/RequestPrivilege';


it('Shows empty RequestPrivilege', () => {
  const tree = renderer
    .create(
      <RequestPrivilege
        groupId={1}
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it('Shows new RequestPrivilege', () => {
  const tree = renderer
    .create(
      <RequestPrivilege
        groupId={1}
        justForTesting
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
