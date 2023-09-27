from typing import List, Optional, Dict
from pandas import DataFrame
from ena_objects.ena_run import EnaRun
from ena_objects.ena_experiment import EnaExperiment
from ena_objects.ena_sample import EnaSample
from ena_objects.ena_std_lib import filter_attribute_by, validate_dict


def study_publication_ids(publication_isa_json: Dict) -> List[int]:
    """Retrieves the pubmed_ids from the ISA JSON

    Args:
        publication_isa_json (Dict): Publication part of the ISA JSON dictionary

    Returns:
        List[int]: List of pubmed ID's
    """
    return [pub["id"] for pub in publication_isa_json]


def study_alias(study_isa_json: str) -> str:
    """Creates a study_alias, based on information of the study part of the ISA JSON.

    Args:
        study_isa_json (str): Study part of the ISA JSON

    Returns:
        str: the study_alias
    """
    prefix = "https://datahub.elixir-belgium.org/studies/"  # TODO: Replace by something less hard-coded
    seek_study_id: str = filter_attribute_by(
        study_isa_json["comments"], key="name", value="SEEK Study ID"
    )[0]["value"]
    return prefix + seek_study_id


class EnaStudy:
    """Generates a Study object, compliant to the requirements of ENA"""

    mandatory_keys = ["title", "description", "publications"]

    def __init__(
        self,
        alias: str,
        title: str,
        study_type: str,
        study_abstract: str,
        runs: List[EnaRun],
        samples: List[EnaSample],
        experiments: List[EnaExperiment],
        new_study_type: Optional[str] = None,
        pubmed_id: Optional[List[int]] = None,
    ) -> None:
        self.alias = alias
        self.title = title
        self.study_type = study_type
        self.new_study_type = new_study_type
        self.study_abstract = study_abstract
        self.runs = runs
        self.samples = samples
        self.experiments = experiments
        self.new_study_type = new_study_type
        self.pubmed_id = pubmed_id

    def __dict__(self):
        return {
            "alias": self.alias,
            "title": self.title,
            "study_type": self.study_type,
            "study_abstract": self.study_abstract,
            "new_study_type": self.new_study_type,
            "pubmed_id": self.pubmed_id,
        }

    def from_isa_json(isa_json: Dict):
        """Method that creates an EnaStudy with params from ISA JSON Dictionary

        Args:
            isa_json: ISA JSON Dict

        Returns:
            EnaStudy: EnaStudy object
        """
        [validate_dict(isa_json, key) for key in EnaStudy.mandatory_keys]

        return [
            EnaStudy(
                alias=study_alias(study),
                title=study["title"],
                study_type="",  # TODO: Replace by Custom metadata of the Assay level
                study_abstract=study["description"],
                runs=None,
                samples=EnaSample.from_study_dict(study),
                experiments=None,
                new_study_type=None,
                pubmed_id=study_publication_ids(
                    publication_isa_json=study["publications"]
                ),
            )
            for study in isa_json["studies"]
        ]

    def to_dataframe(self) -> DataFrame:
        """Dumps the study object in a pandas DataFrame of the object

        Returns:
            DataFrame: Pandas DataFrame representation of the Study
        """
        return DataFrame.from_dict(self.__dict__())
