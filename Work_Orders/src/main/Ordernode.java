package main;
import java.util.ArrayList;
import java.util.List;

public class Ordernode {
	
	private int id;
	private String name;
	private List<Ordernode> dependencies; 
	
	Ordernode(int id, String name) {
		this.id = id;
		this.name = name;
		dependencies = new ArrayList<Ordernode>();
	}

	public int getId() {
		return id;
	}

	public String getName() {
		return name;
	}

	public List<Ordernode> getDependencies() {
		return dependencies;
	}

	public void setDependencies(List<Ordernode> dependencies) {
		this.dependencies = dependencies;
	}
	
	public void addDependency(Ordernode dependency) {
		dependencies.add(dependency);
	}
	
	
}
